# coding: utf-8

"""
This file is a part of asexecutor
https://github.com/efiminem/asexecutor
"""

import os
import stat
import paramiko
from functools import wraps

from asexecutor.client import ExecutorClient
from asexecutor.calculator import RemoteCalculator


class Executor:
    """
    Executes jobs via ssh connection or locally. Can wrap ASE calculators."""

    def __init__(self):
        self.client = ExecutorClient()
        self.jobs = []

    def _connection(func):
        "Decorator for function calls with connection to the server"

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                if self._pkey is not None:
                    self.client.connect(
                        hostname=self.host,
                        username=self.user,
                        pkey=self._pkey,
                        port=self.port,
                    )
                else:
                    self.client.connect(
                        hostname=self.host,
                        username=self.user,
                        password=self.password,
                        port=self.port,
                    )
                result = func(self, *args, **kwargs)
                self.client.close()
                return result
            except paramiko.AuthenticationException:
                print("Authentication failed, please verify your credentials.")
            except paramiko.SSHException as sshException:
                print("Unable to establish SSH connection: {}".format(sshException))
            except paramiko.BadHostKeyException as badHostKeyException:
                print(
                    "Unable to verify server's host key: {}".format(badHostKeyException)
                )
            finally:
                self.client.close()

        return wrapper

    @_connection
    def _get_home_location(self, user):
        "Get home directory of user"
        stdout, stderr = self.client.exec_command(
            'getent passwd "{}" | cut -d: -f6'.format(user)
        )
        return stdout

    def connect(self, host, user, password=None, pkey=None, port=22):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self._pkey = self.client.get_pkey(pkey)
        self.client.remote()
        self.home = self._get_home_location(self.user)[0].strip()

    def disconnect(self):
        self.client.local()

    def status(self):
        """Get status of all jobs initiated by the current instance of executor"""
        print("Name|Host|Partition|Nnodes|Njobs|Start|Time|Finish|Status")
        for job in self.jobs:
            print(
                "{}|{}|{}|{}|{}|{}|{}|{}|{}".format(
                    job.name,
                    job.host,
                    job.partition,
                    job.nnodes,
                    job.njobs,
                    job.start,
                    job.dur_time,
                    job.finish,
                    job.status,
                )
            )

    @_connection
    def execute(self, command):
        """Execute comamnd on server"""
        stdout, stderr = self.client.exec_command(command)
        return stdout, stderr

    @_connection
    def put(self, local_path, remote_path):
        """Move file to the server"""
        sftp = self.client.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()

    def _find_module(self, modules_avail, modulename):
        """Find module among available modules"""
        choices = []
        for elem in modules_avail:
            if modulename in elem:
                choices.append(elem)
        if len(choices) > 0:
            return choices[0]
        raise NameError("Module {} not found on the server.".format(modulename))

    @_connection
    def modules(self):
        """Returns a list of modules available on the server in the order of
        last modification date"""
        stdout, stderr = self.execute("module avail --long")
        if len(stderr) == 0:
            raise NameError("Modules not found on the server.")
        names = []
        dates = []
        for elem in stderr[2:-3]:
            cols = elem.strip().split()
            names.append(cols[0])
            dates.append(cols[-2] + "/" + cols[-1])
        return [
            names[idx[0]]
            for idx in sorted(enumerate(dates), key=lambda x: x[1], reverse=True)
        ]

    @_connection
    def find_modules(self, modulelist):
        """Find modules among available modules on server"""
        result = []
        modules_avail = self.modules()
        for module in modulelist:
            result.append(self._find_module(modules_avail, module))
        return result

    @_connection
    def get(self, remote_path, local_path=None):
        """Get file from server"""

        def _dir_copy_walker(conn, start_path, local_path, depth=0):
            if not os.path.exists(local_path):
                os.mkdir(local_path)
            for fileattr in sftp.listdir_attr(remote_path):
                if stat.S_ISDIR(fileattr.st_mode):
                    if depth < 100:
                        _dir_copy_walker(
                            conn,
                            os.path.join(start_path, fileattr.filename),
                            os.path.join(local_path, fileattr.filename),
                            depth + 1,
                        )
                else:
                    sftp.get(
                        os.path.join(remote_path, fileattr.filename),
                        os.path.join(local_path, fileattr.filename),
                    )

        if local_path is not None and not os.path.isabs(local_path):
            local_path = os.path.join(os.getcwd(), local_path)

        if os.path.isabs(remote_path):
            if local_path is None:
                if self.home not in remote_path:
                    raise NameError(
                        "Path remote_path is ambiguous. You should provide local_path"
                        " also."
                    )
                else:
                    local_path = os.path.join(
                        os.getcwd(), os.path.relpath(remote_path, start=self.home)
                    )
        else:
            if local_path is None:
                local_path = os.path.join(os.getcwd(), remote_path)
            remote_path = os.path.join(self.home, remote_path)

        sftp = self.client.open_sftp()
        if stat.S_ISDIR(sftp.stat(remote_path).st_mode):  # it is a directory
            _dir_copy_walker(sftp, remote_path, local_path)
        else:
            sftp.get(remote_path, local_path)
        sftp.close()
        return local_path

    @_connection
    def mkdirs(self, path):
        """Create directory/ies on server"""
        sftp = self.client.open_sftp()
        partial_path = ""
        for idx, part in enumerate(path.split("/")[1:]):
            partial_path += "/" + part
            try:
                sftp.stat(partial_path)
            except FileNotFoundError:
                sftp.mkdir(partial_path)
        sftp.close()

    @_connection
    def create_file(self, path, name, content):
        """Create file on server with given content"""
        if len(path) == 0:
            raise NameError("Path shouldn't be empty!")
        if len(name) == 0:
            raise NameError("Name shouldn't be empty!")
        try:
            sftp = self.client.open_sftp()
            file = sftp.file(os.path.join(path, name), "a", -1)
            file.write(content)
            file.flush()
            sftp.close()
            return True
        except:
            return False

    def wrap_calc(self, calc, name, **kwargs):
        "Wraps the ase.calculator for execution on remote server"
        return RemoteCalculator(calc, self, name, **kwargs)

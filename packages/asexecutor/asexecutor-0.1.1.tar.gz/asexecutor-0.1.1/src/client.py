# coding: utf-8

"""
This file is a part of asexecutor
https://github.com/efiminem/asexecutor
"""

import paramiko
import subprocess


class ExecutorClient:
    """Client for executor. If in remote regime, it works upon ssh client,
    otherwise it manages local executions"""

    def __init__(self):
        self.client = None
        self.is_remote = False

    def connect(self, *args, **kwargs):
        if self.client is not None:
            self.client.connect(*args, **kwargs)

    def exec_command(self, *args, **kwargs):
        if self.client is not None:
            stdin, stdout, stderr = self.client.exec_command(*args, **kwargs)
            return stdout.readlines(), stderr.readlines()
        else:
            output = subprocess.Popen(
                *args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            stdout, stderr = output.communicate()
            return stdout, stderr

    def open_sftp(self, *args, **kwargs):
        if self.client is not None:
            return self.client.open_sftp()
        return None

    def remote(self):
        self.client = paramiko.SSHClient()
        # we need to add server to known hosts if it's not already there
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.is_remote = True

    def local(self):
        self.client = None
        self.is_remote = False

    def get_pkey(self, filename):
        if filename is None:
            return None
        return paramiko.RSAKey.from_private_key_file(filename)

    def close(self):
        if self.client is not None:
            self.client.close()

# coding: utf-8

"""
This file is a part of asexecutor
https://github.com/efiminem/asexecutor
"""

from asexecutor.schedulers import get_scheduler


class Job:
    """Job for exectuion on the server. Contains implementations
    for different types of schedulers."""

    exclusive_params = [
        "path",
        "host",
        "command",
        "modulelist",
        "scheduler",
        "status",
        "dur_time",
        "start",
        "finish",
        "id",
    ]

    def __init__(
        self,
        path,
        command,
        scheduler,
        host=None,
        name="default",
        nnodes=1,
        njobs=1,
        is_exclusive=False,
        memory=None,
        modulelist=None,
        account=None,
        begin=None,
        exclude=None,
        queue=None,
        nodelist=None,
        status=None,
        time=None,
        dur_time=None,
        start=None,
        finish=None,
        id=None,
        **kwargs
    ):

        # intrinsic job parameters
        self.set_scheduler(scheduler)
        self.path = path
        self.host = host
        self.command = command
        self.modulelist = modulelist
        self.status = status
        self.dur_time = dur_time
        self.start = start
        self.finish = finish
        self.id = id

        # these parameters will be in the job script
        self.name = name
        self.nnodes = nnodes
        self.njobs = njobs
        self.is_exclusive = is_exclusive
        self.memory = memory
        self.account = account
        self.begin = begin
        self.exclude = exclude
        self.queue = queue
        self.time = time
        self.nodelist = nodelist
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def set_scheduler(self, name):
        self.scheduler = get_scheduler(name)

    def get_params(self):
        result = {}
        for key, value in self.__dict__.items():
            if key not in self.exclusive_params and value is not None:
                result[key] = value
        return result

    def compile_params(self):
        return self.scheduler.compile_params(**self.get_params())

    def compile_job(self):
        result = "#!/bin/bash\n"
        result += "#Job is created by asexecutor\n\n"
        result += self.compile_params()
        result += "\n\n"
        if self.modulelist is not None:
            for module in self.modulelist:
                result += "module load " + module + "\n"
        result += "\ncd " + self.path + "\n"
        result += "time " + self.command + "\n\n"
        result += "exit 0"
        return result

    def write_job(self, filename):
        with open(filename, "w") as f:
            f.write(self.compile_job())

    def asdict(self):
        """Return a dictionary representation of the job state."""
        dct = self.__dict__.copy()
        if "scheduler" in dct:
            dct["scheduler"] = dct["scheduler"].name
        return dct

    def fromdict(self, dct):
        """Restore job from a dictionary"""
        self.__dict__ = dct
        if "scheduler" in dct:
            self.set_scheduler(dct["scheduler"])

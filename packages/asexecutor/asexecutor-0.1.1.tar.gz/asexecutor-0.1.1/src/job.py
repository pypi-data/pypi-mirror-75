# coding: utf-8

"""
This file is a part of asexecutor
https://github.com/efiminem/asexecutor
"""


class Job:
    """Job for exectuion on the server. Contains implementations
    for different types of schedulers."""

    implemented_schedulers = ["slurm", "lsf"]
    mem_ptwo = [1125899906842624, 1099511627776, 1073741824, 1048576, 1024, 1]
    mem_pfix_i = ["EiB", "PiB", "TiB", "GiB", "MiB", "KiB"]
    mem_pfix = ["EB", "PB", "TB", "GB", "MB", "KB"]

    def __init__(
        self,
        path,
        command,
        scheduler,
        host=None,
        name="default",
        partition=None,
        nnodes=1,
        njobs=1,
        max_memory=None,
        modulelist=None,
        account=None,
        begin=None,
        exclude=None,
        is_exclusive=False,
        queue=None,
        export=None,
        nodelist=None,
        status=None,
        time=None,
        dur_time=None,
        start=None,
        finish=None,
        id=None,
    ):
        if scheduler not in self.implemented_schedulers:
            raise NameError("Scheduler {} is not implemeted.".format(scheduler))
        self.path = path
        self.command = command
        self.scheduler = scheduler
        self.host = host
        self.name = name
        self.partition = partition
        self.nnodes = nnodes
        self.njobs = njobs
        self.max_memory = max_memory
        self.modulelist = modulelist
        self.account = account
        self.begin = begin
        self.exclude = exclude
        self.is_exclusive = is_exclusive
        self.queue = queue
        self.export = export
        self.nodelist = nodelist
        self.host = host
        self.status = status
        self.dur_time = dur_time
        self.start = start
        self.finish = finish
        self.id = id
        self.time = time
        self.scheduler = scheduler
        self._set_scheduler_params()

    def _set_scheduler_params(self):
        if self.scheduler == "slurm":
            self.scheduler_run_command = "sbatch"
            self.prefix = "#SBATCH"
            self.if_i_in_memory = True
        elif self.scheduler == "lsf":
            self.scheduler_run_command = "bsub"
            self.prefix = "#BSUB"
            self.if_i_in_memory = False

    def _to_mem_rounded(self, memory):
        for idx, ptwo in enumerate(self.mem_ptwo):
            if memory >= ptwo:
                if self.if_i_in_memory:
                    return str(round(memory / ptwo)) + self.mem_pfix_i[idx]
                else:
                    return str(round(memory / ptwo)) + self.mem_pfix[idx]
        return str(memory)

    def write_job(self, filename):
        def write_job_line(f, name, value, option="u", comment=None):
            """Write job line to file. "u" stands for usual option aka -option,
            "l" stands for long option aka --option="""
            if value is not None:
                if option == "u":
                    delim = "-"
                    term = " "
                elif option == "l":
                    delim = "--"
                    term = "="
                else:
                    raise NameError("Option {} is unknow".format(option))
                if isinstance(value, bool):
                    if value == True:
                        f.write("{} {}{}".format(prefix, delim, name))
                elif type(value) in (str, int, float):
                    f.write("{} {}{}{}{}".format(prefix, delim, name, term, value))
                else:
                    if hasattr(value, "__len__"):
                        f.write("{} {}{}{}".format(prefix, delim, name, term))
                        vlength = len(value)
                        for idx, elem in enumerate(value):
                            f.write("{}".format(elem))
                            if idx + 1 != vlength:
                                f.write(",")
                    else:
                        raise NameError(
                            "Cannot recognize input for {}. Value should be bool, int,"
                            " float, string or array-like.".format(name)
                        )
                if comment is not None:
                    f.write(" # {}".format(comment))
                if not (isinstance(value, bool) and value == False):
                    f.write("\n")

        prefix = self.prefix
        with open(filename, "w") as f:
            f.write("#!/bin/bash\n")
            f.write("#Job is created by asexecutor\n\n")
            if self.scheduler == "slurm":
                write_job_line(f, "account", self.account, "l")
                write_job_line(f, "qos", self.queue, "l")
                write_job_line(f, "partition", self.partition, "l")
                write_job_line(f, "job-name", self.name, "l")
                write_job_line(f, "nodes", self.nnodes, "l")
                write_job_line(f, "tasks-per-node", self.njobs, "l")
                write_job_line(f, "exclude", self.exclude, "l")
                write_job_line(f, "nodelist", self.nodelist, "l")
                write_job_line(f, "exclusive", self.is_exclusive, "l")
                if self.max_memory in self.mem_ptwo:
                    write_job_line(f, "mem", self._to_mem_rounded(self.max_memory), "l")
                else:
                    write_job_line(
                        f,
                        "mem",
                        str(self.max_memory) + "KiB",
                        "l",
                        "approx " + self._to_mem_rounded(self.max_memory),
                    )

                write_job_line(f, "begin", self.begin, "l")
                write_job_line(f, "time", self.time, "l")
                write_job_line(f, "export", self.export, "l")
                write_job_line(f, "output", str(self.name) + ".out", "l")
                write_job_line(f, "error", str(self.name) + ".err", "l")

            elif self.scheduler == "lsf":
                write_job_line(f, "P", self.account, "u")
                write_job_line(f, "q", self.queue, "u")
                write_job_line(f, "m", self.partition, "u")
                write_job_line(f, "J", self.name, "u")
                write_job_line(f, "nnodes", self.nnodes, "u")
                r_text = '"span[ptile={}]'.format(self.njobs)
                if self.max_memory is not None:
                    r_text += " rusage[mem={}KB]".format(self.max_memory)
                r_text += '"'
                write_job_line(
                    f,
                    "R",
                    r_text,
                    "u",
                    "approx " + self._to_mem_rounded(self.max_memory),
                )
                write_job_line(f, "W", self.time, "u")
                write_job_line(f, "o", str(self.name) + ".out", "u")
                write_job_line(f, "e", str(self.name) + ".err", "u")

            f.write("\n")
            if self.modulelist is not None:
                for module in self.modulelist:
                    f.write("module load " + module + "\n")
            f.write("\ncd " + self.path + "\n")
            f.write("time " + self.command + "\n\n")
            f.write("exit 0")

    def asdict(self):
        """Return a dictionary representation of the calculator state."""
        dct = self.__dict__.copy()
        dct.pop("scheduler_run_command")
        dct.pop("prefix")
        dct.pop("if_i_in_memory")
        return dct

    def fromdict(self, dct):
        """Restore calculator from a dictionary"""
        self.__dict = dct
        self._set_scheduler_params()

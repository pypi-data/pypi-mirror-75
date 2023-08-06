# coding: utf-8

"""
This file is a part of asexecutor
https://github.com/efiminem/asexecutor
"""

import math
from asexecutor.units import memory_values_IEC
from asexecutor.units import memory_short_names, memory_short_names_IEC
from asexecutor.units import KiB

implemented_schedulers = ["slurm", "lsf", "pbs", "sge"]
SHORT = "s"  # stands for short option aka -option
SHORTEQ = "seq"  # stands for -option=
LONG = "l"  # stands for long option aka --option=


def get_scheduler(scheduler):
    if scheduler == "slurm":
        return SlurmScheduler()
    elif scheduler == "lsf":
        return LSFScheduler()
    elif scheduler == "pbs":
        return PBSScheduler()
    elif scheduler == "sge":
        return SGEScheduler()
    else:
        err_text = "Scheduler {} is not implemented. Available schedulers are ".format(
            scheduler
        )
        slength = len(implemented_schedulers)
        for idx, name in enumerate(implemented_schedulers):
            err_text += name
            if idx + 2 == slength:
                err_text += " and "
            elif idx + 1 != slength:
                err_text += ", "
        err_text += "."
        raise NameError(err_text)


class Scheduler:
    """Abstract class for schedulers"""

    def check_mem(self, memory):
        if memory < KiB:
            raise ValueError(
                "Value of memory should be greater than 1KiB. Provided value: {}B"
                .format(memory)
            )
        return True

    def kb_mem(self, memory):
        if memory % KiB != 0:
            memory = math.ceil(memory / KiB) * KiB
        return memory

    def round_mem(self, memory):
        for idx, ptwo in enumerate(memory_values_IEC[6:0:-1]):
            if memory >= ptwo:
                if self.is_SI:
                    return str(round(memory / ptwo)) + memory_short_names_IEC[6 - idx]
                else:
                    return str(round(memory / ptwo)) + memory_short_names[6 - idx]
        return None

    def beauty_mem(self, memory):
        for idx, ptwo in enumerate(memory_values_IEC[6:0:-1]):
            if memory % ptwo == 0:
                if self.is_SI:
                    return str(memory // ptwo) + memory_short_names_IEC[6 - idx]
                else:
                    return str(memory // ptwo) + memory_short_names[6 - idx]
        return None

    def compile_params_line(self, name, value, option=SHORT, comment=None):
        """Get one line of a script."""
        if option == SHORT:
            delim = "-"
            term = " "
        elif option == SHORTEQ:
            delim = "-"
            term = "="
        elif option == LONG:
            delim = "--"
            term = "="
        else:
            raise NameError("Option {} is unknow".format(option))
        result = ""
        if isinstance(value, bool):
            if value == True:
                result += "#" + self.prefix + " " + delim + name
        elif type(value) in (str, int, float):
            result += "#" + self.prefix + " " + delim + name + term + str(value)
        else:
            if hasattr(value, "__len__"):
                result += "#" + self.prefix + " " + delim + name + term
                vlength = len(value)
                for idx, elem in enumerate(value):
                    result += str(elem)
                    if idx + 1 != vlength:
                        result += ","
            else:
                raise ValueError(
                    "Cannot recognize input for {}. Value should be bool, int,"
                    " float, string or array-like.".format(name)
                )
        if comment is not None:
            result += " # " + str(comment)
        if not (isinstance(value, bool) and value == False):
            result += "\n"
        return result

    def compile_params(self, **kwargs):
        result = ""
        r_params = []
        for key in kwargs.keys():
            if key in self.params:
                true_key, option = self.params[key]
                value = kwargs[key]
                if value is not None:
                    result += self.compile_params_line(true_key, value, option)
            elif hasattr(self, "mem_params") and key in self.mem_params:
                true_key, option = self.mem_params[key]
                value = kwargs[key]
                if value is not None and self.check_mem(value):
                    if isinstance(value, float):
                        value = int(value)
                    if isinstance(value, int):
                        value = self.kb_mem(value)
                        round_value = self.round_mem(value)
                        beauty_value = self.beauty_mem(value)
                        if round_value == beauty_value:
                            result += self.compile_params_line(
                                true_key, round_value, option
                            )
                        else:
                            result += self.compile_params_line(
                                true_key, beauty_value, option, "approx " + round_value,
                            )
                    else:
                        raise ValueError("Value of {} should be int.".format(key))
            elif hasattr(self, "r_params") and key in self.r_params:
                r_params.append((key, kwargs[key]))
            else:
                raise NameError(
                    "Parameter {} is not supported by {} scheduler.".format(
                        key, self.name.capitalize()
                    )
                )
        if hasattr(self, "r_params"):
            r_text = self.compile_r_params(r_params)
            if r_text is not None:
                result += self.compile_params_line("R", r_text, SHORT)
        if "output" not in kwargs:
            true_key, option = self.params["output"]
            result += self.compile_params_line(
                true_key, kwargs["name"] + ".out", option
            )
        if "error" not in kwargs:
            true_key, option = self.params["error"]
            result += self.compile_params_line(
                true_key, kwargs["name"] + ".err", option
            )
        return result.strip()

    def compile_r_params(self, r_params_list):
        if len(r_params_list) == 0:
            return None
        r_params_dict = {}
        r_text = '"'
        for r_param in r_params_list:
            key, subkey = self.r_params[r_param[0]]
            if key not in r_params_dict:
                r_params_dict[key] = []
            r_params_dict[key].append((subkey, r_param[1]))
        rlength = len(r_params_dict)
        for idx, (key, value_list) in enumerate(r_params_dict.items()):
            r_text += key + "["
            vlength = len(value_list)
            for jdx, (subkey, value) in enumerate(value_list):
                if subkey == "mem":
                    value = self.kb_mem(value)
                    value = self.beauty_mem(value)
                r_text += subkey + "=" + str(value)
                if jdx + 1 != vlength:
                    r_text += ","
            r_text += "]"
            if idx + 1 != rlength:
                r_text += " "
        r_text += '"'
        return r_text


class SlurmScheduler(Scheduler):
    """Parameters for Slurm scheduler"""

    name = "slurm"
    prefix = "SBATCH"
    cmd_run = "sbatch"
    is_SI = True

    params = {
        "account": ("account", LONG),
        "begin": ("begin", LONG),
        "error": ("error", LONG),
        "exclude": ("exclude", LONG),
        "is_exclusive": ("exclusive", LONG),
        "is_rerunnable": ("requeue", LONG),
        "name": ("job-name", LONG),
        "njobs": ("tasks-per-node", LONG),
        "nnodes": ("nodes", LONG),
        "nodelist": ("nodelist", LONG),
        "output": ("output", LONG),
        "qos": ("qos", LONG),
        "queue": ("partition", LONG),
        "time": ("time", LONG),
    }

    mem_params = {
        "memory": ("mem", LONG),
    }


class LSFScheduler(Scheduler):
    """Parameters for LSF scheduler"""

    name = "lsf"
    prefix = "BSUB"
    cmd_run = "bsub"
    is_SI = True

    params = {
        "account": ("P", SHORT),
        "affinity": ("jobaff", SHORT),
        "alloc_flags": ("alloc_flags", SHORT),
        "app": ("app", SHORT),
        "ar": ("ar", SHORT),
        "begin": ("b", SHORT),
        "close_signal": ("signal", SHORT),
        "csm": ("csm", SHORT),
        "csm_compute_unit": ("cn_cu", SHORT),
        "csm_core_isolation": ("core_isolation", SHORT),
        "csm_jsm": ("jsm", SHORT),
        "csm_ln_mem": ("ln_mem", SHORT),
        "csm_ln_slots": ("ln_slots", SHORT),
        "csm_mem": ("cn_mem", SHORT),
        "csm_smt_value": ("smt_value", SHORT),
        "csm_step_cgroup": ("step_cgroup", SHORT),
        "core_limit": ("C", SHORT),
        "checkpoint": ("k", SHORT),
        "clusters": ("clusters", SHORT),
        "cpu_time_limit": ("c", SHORT),
        "cwd": ("cwd", SHORT),
        "data": ("data", SHORT),
        "data_limit": ("D", SHORT),
        "dependency": ("w", SHORT),
        "description": ("Jd", SHORT),
        "env": ("env", SHORT),
        "eptl": ("eptl", SHORT),
        "error": ("e", SHORT),
        "estimated_time": ("We", SHORT),
        "esub": ("a", SHORT),
        "exit_code": ("Q", SHORT),
        "extsched": ("extsched", SHORT),
        "file_limit": ("F", SHORT),
        "freq": ("freq", SHORT),
        "host_file": ("hostfile", SHORT),
        "input": ("i", SHORT),
        "is_enforcement": ("hl", SHORT),
        "is_exclusive": ("x", SHORT),
        "is_rerunnable": ("r", SHORT),
        "is_suspended": ("H", SHORT),
        "job_group_name": ("g", SHORT),
        "local_file operator": ("f", SHORT),
        "login_shell": ("L", SHORT),
        "ls_project_name": ("Lp", SHORT),
        "mem_per_task": ("M", SHORT),
        "migration_threshold": ("mig", SHORT),
        "name": ("J", SHORT),
        "network_res_req": ("network", SHORT),
        "nnodes": ("nnodes", SHORT),
        "nodelist": ("m", SHORT),
        "notify": ("notify", SHORT),
        "nthreads": ("T", SHORT),
        "output": ("o", SHORT),
        "pending_limit": ("ptl", SHORT),
        "post_exec_command": ("post_exec_command", SHORT),
        "pre_exec_command": ("pre_exec_command", SHORT),
        "priority": ("sp", SHORT),
        "process_limit": ("p", SHORT),
        "queue": ("q", SHORT),
        "reservation": ("U", SHORT),
        "resize_notification_cmd": ("rnc", SHORT),
        "service_class_name": ("sla", SHORT),
        "spool": ("Zs", SHORT),
        "stack_limit": ("S", SHORT),
        "stage": ("stage", SHORT),
        "swap": ("swap", SHORT),
        "time": ("W", SHORT),
        "use_user_limits": ("ul", SHORT),
        "user_group": ("G", SHORT),
        "warning_action": ("wa", SHORT),
        "warning_time": ("wt", SHORT),
    }

    r_params = {
        "njobs": ["span", "ptile"],
        "memory": ["rusage", "mem"],
    }


class PBSScheduler(Scheduler):
    """Parameters for PBS scheduler"""

    name = "pbs"
    prefix = "PBS"
    cmd_run = "qsub"
    is_SI = True

    params = {
        "account": ("W group_list", SHORTEQ),
        "begin": ("A", SHORT),
        "error": ("e", SHORT),
        "is_exclusive": ("l naccesspolicy=singlejob", SHORT),
        "is_rerunnable": ("r", SHORT),
        "name": ("N", SHORT),
        "njobs": ("l ppn", SHORTEQ),
        "nnodes": ("l nodes", SHORTEQ),
        "output": ("o", SHORT),
        "queue": ("q", SHORT),
        "qos": ("l qos", SHORTEQ),
        "time": ("l walltime", SHORTEQ),
    }

    mem_params = {
        "memory": ("l mem", SHORTEQ),
    }


class SGEScheduler(Scheduler):
    """Parameters for SGE scheduler"""

    name = "sge"
    prefix = "$"
    cmd_run = "qsub"
    is_SI = True

    params = {
        "begin": ("a", SHORT),
        "error": ("e", SHORT),
        "is_exclusive": ("l exclusive", SHORT),
        "is_rerunnable": ("r", SHORT),
        "name": ("N", SHORT),
        "njobs": ("pe", SHORT),
        "nnodes": ("l nodes", SHORTEQ),
        "output": ("o", SHORT),
        "queue": ("q", SHORT),
        "time": ("l h_rt", SHORT),
    }

    mem_params = {
        "memory": ("l mem_free", LONG),
    }

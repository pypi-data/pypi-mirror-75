# coding: utf-8

"""
This file is a part of asexecutor
https://github.com/efiminem/asexecutor
"""

import os
from datetime import datetime
from ase.io import jsonio
from ase.calculators.calculator import Calculator, all_changes
from ase.calculators.calculator import CalculatorSetupError, PropertyNotImplementedError

from asexecutor.job import Job
from asexecutor.units import GiB


class RemoteCalculator(Calculator):
    """Wraps the ase.calculator for execution"""

    implemented_calculators = ["Vasp2"]
    implemented_schedulers = ["slurm", "lsf"]

    name = "RemoteCalculator"
    ase_objtype = "remote_calculator"  # For JSON storage

    def __init__(
        self,
        calc,
        executor,
        name="default",
        task_dir="tasks",
        scheduler="slurm",
        allow_submit=True,
        **kwargs
    ):
        if calc.name not in self.implemented_calculators:
            raise CalculatorSetupError(
                "Wrapper is not implemented for calculator {}.".format(calc.name)
            )
        if scheduler not in self.implemented_schedulers:
            raise CalculatorSetupError(
                "Scheduler {} is not implemeted.".format(scheduler)
            )
        Calculator.__init__(self)
        self.executor = executor
        self.implemented_properties = calc.implemented_properties
        self.default_parameters = calc.default_parameters
        self.calc = calc
        self.directory = calc.directory
        self.name = name
        self.task_dir = task_dir
        self.scheduler = scheduler
        self.allow_submit = allow_submit
        self.kwargs = kwargs
        self.job = None
        self.path = None

        # Here we correct a typo in old version of VASP2 calculator where was
        # 'verison' in initialization instead of 'version'. It didn't allow to
        # save calculator's state when it is not finished.
        self.calc.version = None

    def calculate(self, atoms=None, properties=["energy"], system_changes=all_changes):
        """Do a calculation in the specified directory on server.

        This will generate the necessary input files, send them to the cluster
        and then execute. After execution, the output files are received
        back from the server and the energy, forces. etc. are read."""

        if self.job is None:

            # Note: in order to do the structural changes to the initial Atoms object
            # we can write:
            #
            # initial_atoms.calc = calc # optional, but allows to calculate
            #                           # properties afterwards
            # calc.calculate(initial_atoms)
            #
            # If we are not going to change the structure it is better to use
            # the following construction:
            #
            # initial_atoms.calc = calc
            # initial_atoms.get_energy()
            #

            Calculator.calculate(self.calc, atoms, properties, system_changes)

            # We intentianally keep self.atoms = None until the calculation is done.
            # It makes get_property method to go back to the current method because
            # check_state will always return all_changes.
            #
            # self.atoms = self.calc.atoms
            #

            self.calc.check_cell()  # Check for zero-length lattice vectors
            self.calc._xml_data = None  # Reset the stored data

            self.calc.write_input(self.calc.atoms, properties, system_changes)

            start_time = datetime.now()
            curr_task_dir = self.name + start_time.strftime("-%Y-%m-%d-")
            abs_task_dir = os.path.join(self.executor.home, self.task_dir)
            self.executor.mkdirs(abs_task_dir)
            stdout, stderr = self.executor.execute(
                "cd {}; ls -d {}* | sort -V | tail -1".format(
                    abs_task_dir, curr_task_dir
                )
            )
            if len(stderr) != 0:
                if "No" in stderr[0]:  # file pattern doesn't exist
                    curr_task_dir += "1"
                else:
                    raise CalculatorSetupError(stderr[0])
            if len(stdout) != 0:
                curr_task_dir += str(int(stdout[0].split("-")[-1]) + 1)
            self.path = os.path.join(self.executor.home, self.task_dir, curr_task_dir)
            # we attempt to set some parameters automatically
            if "modulelist" not in self.kwargs:
                self.kwargs["modulelist"] = self.executor.find_modules(
                    ["mkl", "impi", "vasp"]
                )
            if "command" not in self.kwargs:
                self.kwargs["command"] = "mpirun vasp_std"
            if "njobs" not in self.kwargs:
                self.kwargs["njobs"] = 8
            if "memory" not in self.kwargs:
                self.kwargs["memory"] = 10*GiB
            self.job = Job(
                name=self.name,
                path=self.path,
                scheduler=self.scheduler,
                host=self.executor.host,
                status="not submitted",
                **self.kwargs
            )
            self.job.write_job(
                os.path.join(self.calc.directory, self.name + "." + self.scheduler)
            )
            self.submit()

        elif self.job.status == "not submitted":
            self.submit()

        elif self.job.status != "completed":
            status, dur_time, start, finish = self.get_status()
            self.job.status = status
            self.job.dur_time = dur_time
            self.job.start = start
            self.job.finish = finish
            if self.job.status != "completed":
                print(
                    "Job {} is {} on the cluster.".format(self.name, self.job.status),
                    end="",
                )
                if self.job.status == "running":
                    print(" ({})".format(self.job.dur_time))
                else:
                    print()
            else:
                self.executor.get(self.path, self.calc.directory)

                # we can loose some parameters when we save results and job is not finished
                if not hasattr(self.calc, "resort"):
                    self.initialize(atoms)

                self.calc.update_atoms(atoms)
                self.calc.read_results()
                self.results = self.calc.results

                # Now we are not going back to the current method
                self.atoms = self.calc.atoms

        # Here we handle the case where calculator is loaded from json and the atoms object,
        # which is passed to the calculator, needs to be changed
        elif self.job.status == "completed":
            if atoms is not None and self.atoms is not None:
                atoms.positions = self.atoms.positions
                atoms.cell = self.atoms.cell

        # Hacky way to ignore the 'not present' error if calculation is not ready
        if self.job is None or (
            self.job is not None and self.job.status != "completed"
        ):
            for prop in properties:
                self.results[prop] = None
            # all of these properties are present anyway
            vasp_properties = [
                "energy",
                "forces",
                "stress",
                "free_energy",
                "magmom",
                "magmoms",
                "dipole",
                "nbands",
            ]
            for prop in vasp_properties:
                self.results[prop] = None

    def submit(self):
        """Submits the job to the cluster"""
        if self.job is not None:
            if self.allow_submit == True:
                self.executor.mkdirs(self.path)
                for filename in os.listdir(self.calc.directory):
                    self.executor.put(
                        os.path.join(self.calc.directory, filename),
                        os.path.join(self.path, filename),
                    )
                stdout, stderr = self.executor.execute(
                    "cd {}; {} {}.{}".format(
                        self.path, self.job.scheduler.cmd_run, self.name, self.scheduler
                    )
                )
                if len(stderr) != 0:
                    raise CalculatorSetupError(stderr[0])
                response = stdout[0]
                if "Submitted batch job " in response:
                    print("Job {} is submitted to the cluster.".format(self.name))
                    self.job.status = "submitted"
                    self.job.id = int(response.replace("Submitted batch job ", ""))
                    self.executor.jobs.append(self.job)
                else:
                    print(
                        "Failed to submit the job {} to the cluster.".format(self.name)
                    )
            else:
                print(
                    "Job {} was created but not submitted (allow_submit = False)."
                    .format(self.name)
                )

        else:
            raise ValueError("There is no job to submit.")

    def cancel(self):
        """Cancels the job initiated by calculator"""
        if self.job is not None:
            stdout, stderr = self.executor.execute("scancel {}".format(self.job.id))
            status, dur_time, start, finish = self.get_status()
            self.job.status = "cancelled"
            self.job.dur_time = dur_time
            self.job.start = start
            self.job.finish = finish
            print(
                "Job {} is cancelled on the cluster.".format(self.name, self.job.status)
            )

    def get_status(self):
        """Gets status of job on the server"""
        stdout, stderr = self.executor.execute(
            "sacct -X -p -j {} --format=state,elapsed,start,end".format(self.job.id)
        )
        if len(stderr) != 0:
            raise CalculatorSetupError(stderr[0])
        status, dur_time, start, finish = stdout[1].strip()[:-1].split("|")
        if "cancelled" in status.lower():
            status = "cancelled"
        if dur_time == "00:00:00":
            dur_time = None
        if start == "Unknown":
            start = None
        if finish == "Unknown":
            finish = None
        return status.lower(), dur_time, start, finish

    def set_atoms(self, atoms):
        if hasattr(self.calc, "set_atoms"):
            self.calc.set_atoms(atoms)

    def asdict(self):
        """Return a dictionary representation of the calculator state."""
        dct = self.calc.asdict()
        if self.job is not None:
            dct["job"] = self.job.asdict()
        return dct

    def fromdict(self, dct):
        """Restore calculator from a dictionary"""
        self.calc.fromdict(dct)
        if "job" in dct:
            self.job = Job(**dct["job"])
            self.path = self.job.path
            if self.job.status == "completed":
                self.atoms = self.calc.atoms
            self.results = self.calc.results

    def write_json(self, filename):
        """Dump calculator state to JSON file."""
        filename = os.path.join(self.directory, filename)
        dct = self.asdict()
        jsonio.write_json(filename, dct)

    def read_json(self, filename):
        """Load Calculator state from an exported JSON file."""
        dct = jsonio.read_json(filename)
        self.fromdict(dct)

    def __getattr__(self, attr):
        """We pass everything we don't handle to the child calculator"""
        if hasattr(self.calc, attr):

            def wrapper(*args, **kwargs):
                return getattr(self.calc, attr)(*args, **kwargs)

            return wrapper
        raise AttributeError(attr)

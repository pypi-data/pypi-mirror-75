"""
Module that manage experiences, from parameters to grid executions
"""

from itertools import product
from collections import defaultdict
from copy import deepcopy
from os import environ
import os
from sys import argv, executable
import pickle
import subprocess
import time


class ExperienceBase(object):
    """
    Base class for experience
    """

    def __init__(
        self,
        python_executable=executable,
        script_name=None,
        save_filename="latest.pkl",
        job_filename="latest.job",
        output_dir="output",
        job_name="latest",
    ):
        """
        Instanciate the base class for ExperienceBase.
        Keyword arguments:
        python_executable -- which python to use
        script_name -- the name of the script to run through the grid, default is itself
        save_filename -- filename for saving parameters
        job_filename -- filename of the job generated
        output_dir -- the folder which stderr and stdout from job will be created
        job_name -- the name of the job
        """

        self._python_executable = python_executable
        self._script_name = script_name if script_name is not None else argv[0]
        self._save_filename = save_filename
        self._job_filename = job_filename
        self._output_dir = output_dir
        self._job_name = job_name

        self._sub_namespace_dict = defaultdict(dict)
        self._sub_exclusive_namespace_dict = defaultdict(dict)
        self._experience_dict = {}
        self._grid_parameters = []
        self._export_parameters = []
        self._script_parameters = []

        # import only if we instanciate ExperienceBase
        from jinja2 import Environment
        from jinja2 import FileSystemLoader

        package_directory = os.path.dirname(os.path.abspath(__file__))
        j2_template_path = os.path.join(package_directory, "jinja2_templates")
        j2_env = Environment(
            loader=FileSystemLoader(j2_template_path), trim_blocks=False
        )
        self._template = j2_env.get_template("grid_template.j2")

        self.add_export_parameter("RUNNING_IN_SGE", "1")
        self.add_grid_parameter("-e", self._output_dir)
        self.add_grid_parameter("-o", self._output_dir)

    def add_experience_key_values(self, key, values):
        """
        add to the experience some key/values to iterate over (GridSearch)
        Keyword arguments:
        key -- name of that serie
        values -- list of parameters to iterate and combine with others
        """
        self._experience_dict[key] = deepcopy(values)

    def add_experience_namespace_key_values(self, namespace, key, values):
        """
        add to the experience some key/values to iterate over (GridSearch) for a specific namespace
        Keyword arguments:
        namespace -- namespace of that serie
        key -- name of that serie
        values -- list of parameters to iterate and combine with others
        """
        self._sub_namespace_dict[namespace][key] = deepcopy(values)

    def add_experience_exclusive_namespace_key_values(self, namespace, key, values):
        """
        add to the experience some key/values to iterate over (GridSearch) for a specific namespace
        Only one exclusive namespace per experience
        Keyword arguments:
        namespace -- exclusive namespace of that serie
        key -- name of that serie
        values -- list of parameters to iterate and combine with others
        """
        self._sub_exclusive_namespace_dict[namespace][key] = deepcopy(values)

    def add_grid_parameter(self, name, value):
        """
        add grid SGE parameter
        Keyword arguments:
        name -- name of the parameter
        value -- value of the parameter
        """
        if name == "-N":
            self._job_name = value
        else:
            self._grid_parameters.append({"name": name, "value": value})

    def add_export_parameter(self, name, value):
        """
        add bash export for creating new env
        Keyword arguments:
        name -- name of the parameter
        value -- value of the parameter
        """
        self._export_parameters.append({"name": name, "value": value})

    def add_script_parameter(self, param):
        """
        add positional parameter for the experience script
        Keyword arguments:
        param -- parameter to give
        """
        self._script_parameters.append(param)

    def run(self, sync=False):
        """
        run the experience with SGE
        """
        if not self.is_in_SGE():  # in case of bad usage, avoid grid-bombing...
            self._generate_jobfile()
            commands = "\n".join(
                [
                    "source /idiap/home/$(whoami)/.bashrc",
                    "mkdir -p {}".format(self._output_dir),
                    "SETSHELL grid",
                    "qsub {}".format(self._job_filename),
                ]
            )
            if sync:
                commands = commands.replace("qsub", "qsub -sync y")

            process = subprocess.Popen(
                "/bin/bash", stdin=subprocess.PIPE, stdout=subprocess.PIPE
            )
            out, err = process.communicate(commands.encode("utf-8"))
        else:
            print("you try to launch job inside a job!!! please use is_in_SGE")

    def wait_until_finish(self):
        print("deprecated, use run(sync=True) instead")
        time.sleep(3)
        start = time.time()
        print("waiting jobs to finish", end="", flush=True)
        while True:
            self._generate_jobfile()
            commands = "\n".join(
                [
                    "source /idiap/home/$(whoami)/.bashrc",
                    "mkdir -p {}".format(self._output_dir),
                    "SETSHELL grid",
                    "qstat -u '*' | grep $(whoami) | grep {} | wc -l".format(
                        self._job_name
                    ),
                ]
            )

            process = subprocess.Popen(
                "/bin/bash", stdin=subprocess.PIPE, stdout=subprocess.PIPE
            )
            out, err = process.communicate(commands.encode("utf-8"))
            print(".", end="", flush=True)
            if int(out) == 0:
                print("\nDone")
                print("Took {:.2f} seconds".format(time.time() - start))
                return
            time.sleep(1)

    def _generate_jobfile(self):
        """
        Generate the jobfile for run the configured experiment

        Keyword arguments:
        filename -- the name of the jobfile that the experience will output
        """
        experience_dict_copy = deepcopy(self._experience_dict)
        self._grid_parameters.append({"name": "-N", "value": self._job_name})
        for namespace, sub_dict in self._sub_namespace_dict.items():
            experience_dict_copy[namespace] = list(dict_product(sub_dict))
        experience_parameter_product = list(dict_product(experience_dict_copy))
        final_experience_parameters = []
        for exclusive_namespace, sub_dict in self._sub_exclusive_namespace_dict.items():
            namespace_product = list(dict_product(sub_dict))
            for item in experience_parameter_product:
                for namespace_product_instance in namespace_product:
                    item_copy = deepcopy(item)
                    item_copy[exclusive_namespace] = namespace_product_instance
                    final_experience_parameters.append(item_copy)
        if len(final_experience_parameters) == 0:
            final_experience_parameters = experience_parameter_product

        nb_params = len(final_experience_parameters)
        self._save(final_experience_parameters)
        self.add_grid_parameter("-t", "1-{}:1".format(nb_params))
        with open(self._job_filename, "w") as f:
            f.write(
                self._template.render(
                    grid_parameters=self._grid_parameters,
                    export_parameters=self._export_parameters,
                    python_executable=self._python_executable,
                    script_name=self._script_name,
                )
            )

    def _save(self, obj):
        with open(self._save_filename, "wb") as f:
            pickle.dump(obj, f)

    @classmethod
    def _load_all(cls, save_filename="latest.pkl"):
        """
        Load all the parameters, normally you shouldn't need to call this
        """
        with open(save_filename, "rb") as f:
            return pickle.load(f)

    @classmethod
    def load_only_current(cls, save_filename="latest.pkl"):
        """
        Load only the parameter for the current job
        """
        with open(save_filename, "rb") as f:
            return pickle.load(f)[int(environ["SGE_TASK_ID"]) - 1]

    @classmethod
    def is_in_SGE(cls):
        """ Tell if we are running from the SGE and ExperienceBase """
        return "RUNNING_IN_SGE" in environ and str(environ["RUNNING_IN_SGE"]) == "1"


def dict_product(dicts):
    """ combine dicts into single list of dict entries
    inspired from https://stackoverflow.com/questions/5228158/cartesian-product-of-a-dictionary-of-lists/40623158#40623158
    """
    return (dict(zip(dicts, x)) for x in product(*dicts.values()))


if __name__ == "__main__":
    # simple use case
    if ExperienceBase.is_in_SGE():
        current_exp = ExperienceBase.load_only_current()
        print("do your stuff")
        print(str(current_exp))
    else:
        print("Create the experience")
        my_experience = ExperienceBase(
            python_executable="/idiap/user/wdroz/pythonenv/iceberg_gpu/bin/python3"
        )

        my_experience.add_experience_key_values("windows_size", [3, 10])
        my_experience.add_experience_key_values("future_step", [1, 10])

        # my_experience.add_grid_parameter('-l', 'q_short_gpu')
        my_experience.add_grid_parameter("-cwd", "")
        my_experience.add_grid_parameter("-N", "toto_exp")

        my_experience.add_export_parameter("PYTHONPATH", ".:$PYTHONPATH")
        my_experience.add_export_parameter(
            "LD_LIBRARY_PATH", "/idiap/temp/wdroz/cudnn5.1/cuda/lib64:$LD_LIBRARY_PATH"
        )

        my_experience.run()

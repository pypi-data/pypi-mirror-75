
from subprocess import call
from os import path, makedirs
from .generateunittests import main


class Generator:

    def __init__(self, argument):
        self.module_dir = argument.module
        self.output_dir = argument.test_module
        self.argument = argument

    def start(self):
        output_dir = self.output_dir
        if self.output_dir is None:
            output_dir = path.join(self.module_dir, "../test")

        if not path.isdir(output_dir):
            makedirs(output_dir)

        # print(self.argument.module)

        main(self.argument)

        # shell_script = "python -m PyTestStub.GenerateUnitTests -f -m {1} {0} >/dev/null 2>&1".format(
        #     self.module_dir, output_dir)

        # call(shell_script, shell=True)

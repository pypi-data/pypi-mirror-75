import os
import json

from pySpack.core.exec_cmd import exec_cmd


class PySpack:
    SPACK_ROOT = os.getenv("SPACK_ROOT", "/home/ubuntu/spack")
    SPACK_BIN = os.path.join(*(SPACK_ROOT, "bin", "spack"))

    def __init__(self):
        if not os.path.exists(self.SPACK_ROOT):
            raise Exception(f"Cannnot found spack dir: {self.SPACK_ROOT}")

    def __call__(self, *args, **kwargs,):
        # TODO @NexSabre: Change this call for something else
        installation_status = self.install(*args, **kwargs)
        text = f"spack install {args[0]}"
        if not installation_status:
            print(f"failed : {text}")
        else:
            print(f"success: {text}")

    def find(self, package_name) -> bool:
        install_output = exec_cmd(self.SPACK_BIN, ['find', '--json', package_name])
        # noinspection PyBroadException
        try:
            json_information = json.loads(install_output.stdout.decode('utf-8'))
        except:
            return False
        for x in json_information:
            if x["name"] == package_name:
                return True

    def is_installable(self, package_name) -> bool:
        install_output = exec_cmd(self.SPACK_BIN, ['list', package_name])

        return package_name in install_output.stdout.decode('utf-8').split('\n')

    def install(self, *args, print_stdout: bool = False):
        def decode(log, split: bool = True):
            if split:
                return log.decode("utf-8").split("\n")
            return log.decode("utf-8")

        install_output = exec_cmd(self.SPACK_BIN, ['install', *args])

        if install_output.stdout and print_stdout:
            for line in decode(install_output.stdout):
                print(line)

        if install_output.stderr and print_stdout:
            for line in decode(install_output.stdout):
                print(line)

        if install_output.returncode != 0:
            if install_output.stderr:
                print(decode(install_output.stderr))
            return False
        return True

    def uninstall(self, package_name, print_stdout: bool = False) -> bool:
        def decode(log, split: bool = True):
            if split:
                return log.decode("utf-8").split("\n")
            return log.decode("utf-8")

        if not self.find(package_name):
            return True

        install_output = exec_cmd(self.SPACK_BIN, ['uninstall', '-y', package_name])
        if install_output.stdout and print_stdout:
            for line in decode(install_output.stdout):
                print(line)

        if install_output.stderr and print_stdout:
            for line in decode(install_output.stdout):
                print(line)

        if install_output.returncode != 0:
            if install_output.stderr:
                print(decode(install_output.stderr))
            return False
        
        if self.find(package_name):
            return False
        return True

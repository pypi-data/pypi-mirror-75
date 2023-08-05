from subprocess import run, PIPE, STDOUT

import pytest

collect_ignore = ["setup.py"]

from smls.constants import PACKAGE_NAME


def execute_terminal_command(command):
    result = run(command, stdout=PIPE, stderr=STDOUT)
    return result.stdout.decode("utf-8")


@pytest.fixture(autouse=True, scope="session")
def install_the_package():
    execute_terminal_command(["pip", "install", "--editable", "."])
    yield
    execute_terminal_command(["pip", "uninstall", "-y", PACKAGE_NAME])

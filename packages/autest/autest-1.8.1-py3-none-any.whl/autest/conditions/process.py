import json
import os
import re
import subprocess
from typing import Union, List, Callable, Any, Optional
import autest.api as api
import autest.common.is_a as is_a
import autest.common.ospath as ospath
import autest.common.version as verlib
import autest.common.win32 as win32
import hosts.output as host


def HasPythonPackage(self, package: Union[str, List[str]], msg: str):
    '''
    Returns a condition that test if a python package is installed by calling the current active pip.

    Args:
        package: One or more packages to test for. The input can be a space seperated string or a list.
        msg: The message to print if the packages are not found

    Examples:

        Test to see if requests is installed.

        .. code:: python3

            Test.SkipUnless(Condition.HasProgram.HasPythonPackage("requests"))

        Test to see if requests and microserver is installed.

        .. code:: python3

            Test.SkipUnless(Condition.HasProgram.HasPythonPackage("requests microserver"))

        or via a list.

        .. code:: python3

            Test.SkipUnless(Condition.HasProgram.HasPythonPackage(["requests","microserver"]))

    '''
    def _check(output):
        output= output.split("\n")[0]
        lst = json.loads(output)
        for i in lst:
            if i['name'] == package:
                return True
            return False

    return self.CheckOutput(
        ["pip", "list", "--format", "json"],
        _check,
        msg.format(package=package),
        shell=False
    )


def IsElevated(self, msg: str, pass_value:int=0):    # default pass value of 0 == os.geteuid (which for root is 0)
    '''
    Returns a condition that test AuTest is running as a privilege process.
    On Unix based systems this mean root permission
    On Window this mean running with admin rights

    Args:
        msg: The message to print the condition fails
        pass_value: advance value used to control what value is tested when checking the result of running privilege
    '''
    if os.name == 'nt':
        return self.Condition(
            lambda: win32.user_is_admin(),
            msg,
            pass_value
        )
    elif os.name == 'posix':
        return self.Condition(
            lambda: os.geteuid(),
            msg,
            pass_value
        )
    else:
        raise OSError("OS not identified. Can't check for elevated privilege.")


def RunCommand(self, command: str, msg: str, pass_value: int=0, env=None, shell=False):
    '''
    Returns a condition that will run a command and test that return code matches the expected value.
    Use this to run custom command to test for state or to build more custom condition when creating an extension.

    Args:
        command: The command string with anyarguments
        msg: The message to print the condition fails
        pass_value: value to test for the condition to pass
        env: optional environment to use for running the command
        shell: run the command in a shell vs running it without a shell

    '''

    # todo fix to support env arg

    return self.Condition(
        lambda: subprocess.call(command, shell=shell),
        msg,
        pass_value
    )


def CheckOutput(self, command: str, check_func: Callable[[str], bool], msg: str, pass_value: Any=True, neg_msg:Optional[str]=None, shell:bool=False):
    '''
    Returns a condition that will run a command and test the output via a callback function.
    The condition test will pass given that the command run without error
    and the return code of the function provided by the check_func argument matches the pass_value.

    Args:
        command: The command to run
        check_func: The callback function used to test the output of the command.
        msg: The message to print about the condition.
        pass_value: Value to test for the condition to pass.
        env: Optional environment to use for running the command.
        neg_msg: Option message to print if the condition fails.
        shell: Run the command in a shell vs running it without a shell.

    '''
    def check_logic():
        try:
            host.WriteVerbose(["setup"], "Running command:\n", command)
            output = subprocess.check_output(
                command, universal_newlines=True,
                stderr=subprocess.STDOUT,
                shell=shell
            )
        except (subprocess.CalledProcessError, OSError):
            host.WriteVerbose(["setup"], "Command Failed")
            return False
        return check_func(output)

    return self.Condition(
        check_logic,
        msg,
        pass_value,
        neg_msg
    )


def EnsureVersion(self, command, min_version=None, max_version=None, msg=None, output_parser: Optional[Callable[[str], Union[str,None]]]=None, shell=False):
    '''
    Returns a condition that will run a command and test the output matches a predefined version match callback.

    Args:
        command:
            The command to run to get the version value
            The common form of this is `<program> --version` or `<program> -v`
        min_version:
            Optional minimum version that we much match.
            If not provided and value less or equal to the max version will be accepted
        max_version:
            Optional maximum version that we much match.
            If not provided and value greater or equal to the min version will be accepted

            Note:
                One value for min_version or max_version has to be provided.
                Both cannot be None.

        msg: The message to print about the condition.
        output_parser:
            Optional callback function that can be used retrieve the version.
            The default function run a regular expression of "(?P<ver>\d+\.\d+(?:\.\d+)*)"
            If this does not work for the application being tested a custom function can be provided here.
            The function will be given a string of the out of the command to parse.
            It has to return back a string with the version value in it or None is it failed to parse the value.
        pass_value: Value to test for the condition to pass.
        env: Optional environment to use for running the command.
        neg_msg: Option message to print if the condition fails.
        shell: Run the command in a shell vs running it without a shell.


    .. code:: python3

        Test.SkipIf(Condition.EnsureVersion(['curl','--version']),"7.47.0')

    '''

    has_min = False
    has_max = False

    if min_version:
        has_min = True
    else:
        min_version = "*"

    if max_version:
        has_max = True
    else:
        max_version = "*"

    if not has_min and not has_max:
        host.WriteError(
            "Invalid arguments - min_version or max_version must be set", stack=host.getCurrentStack(1)
        )

    def default(output):
        '''
        reg-expression to get version
        '''
        out = re.search(r'(?P<ver>\d+\.\d+(?:\.\d+)*)', output, re.MULTILINE)
        if out:
            return out.groupdict()['ver']
        return None

    # set output parser
    if not output_parser:
        output_parser = default

    def version_check(output):

        # turn our version to an version object
        ver_rng = verlib.VersionRange(
            "[{min}-{max}]".format(min=min_version, max=max_version))
        # call parser to get version value
        ver = output_parser(output)
        # check that it is not None and it matches the range
        if ver and ver in ver_rng:
            return True
        return False

    if not msg:
        msg = "{command} needs to be"
        if has_min and min_version != "*":
            msg += " >= to version: {min_version}"
        if has_min and has_max:
            msg += " and"
        if has_max and max_version != "*":
            msg += " <= version {max_version}"

    if is_a.List(command):
        cmd = command[0]
    else:
        cmd = command.split()[0]

    return self.CheckOutput(
        command,
        version_check,
        msg.format(command=cmd, min_version=min_version,
                   max_version=max_version),
        shell=False
    )


def HasProgram(self, program: str, msg, pass_value=True, path=None):
    '''
    Returns a condition that will test is a application can be found on the path.

    Args:
        program:
            The program to test for.
            On windows .exe does not need to be added as the default
            environment variable of **PATHEXT** will be used.
        msg:
            The message to print about the condition.
        pass_value:
            Value to test for the condition to pass.
            In this case True is for program was found and False for when the it was not.
        path:
            optional string of extra paths to check for the application
            the path most be formatted as the local system PATH variable with the local use of ':' or ';'



    '''
    return self.Condition(lambda: ospath.has_program(program, path), msg, pass_value)


api.ExtendCondition(RunCommand)
api.ExtendCondition(CheckOutput)
api.ExtendCondition(EnsureVersion)
api.ExtendCondition(HasProgram)
api.ExtendCondition(IsElevated)
api.ExtendCondition(HasPythonPackage)

from __future__ import absolute_import, division, print_function
import hosts.output as host
from autest.common.constructor import call_base, smart_init
from autest.core.testentity import TestEntity
import autest.testers as testers
from .process import Process


@smart_init
class Processes(TestEntity):

    @call_base(TestEntity=("runable", ))
    def __init__(self, runable):

        self.__processes = {}
        # this the process we will be viewed as the primary process for the
        # test run
        # if not set we will use try to start the correct based on the
        # order logic
        self.__default = None

    def _Dict(self):
        return self.__processes

    @property
    def _Items(self):
        return self.__processes.values()

    @property
    def _has_default(self):
        return self.__default != None

    def Process(
            self,
            name,
            cmdstr=None,
            returncode=None,
            startup_timeout=10,  # default to 10 second as most things should be ready by this time
    ):
        '''
        Define a new process for the test handle.

        Args:
            name: The name of the process to run. This is just an identifier to use to refer to the process object
            cmdstr: Optional command to run for this process. This can be define latter via the Command property
            returncode: Optional value to test the process return code value with
            startup_timeout: Optional amount of time in seconds for autest to wait for the process to start and be considered ready before erroring out.

        '''
        # todo ... add check to make sure id a variable safe

        # create Process object
        tmp = Process(self._Runable, name, cmdstr)

        # set some global settings before the user might override these locally
        tmp.ForceUseShell = self._Runable.ComposeVariables().Autest.ForceUseShell

        # update setting based on values passed in
        if returncode is not None:
            tmp.ReturnCode = returncode

        tmp.StartupTimeout = startup_timeout

        if name in self.__processes:
            host.WriteWarning("Overriding process object {0}".format(name))
        self.__processes[name] = tmp
        self.__dict__[name] = tmp
        return tmp

    # def Add(self, process):
    #     if self.process.Name in self.__processes:
    #         host.WriteWarning("Overriding process object {0}".format(
    #             self.process.Name))
    #     self.__processes[self.process.Name] = self.process
    #     self.__dict__[self.process.Name] = self.process

    @property
    def Default(self):
        '''
        The process that would be run by default.

        .. note::

            Only the default process will be run by default.
            Processes defined at a test level don't have to define a default process.
            Processes define as part of the TestRun object must define a default process.
            Other process will not start by default and have to be define to StartBefore or StartAfter the default process
            or a process the is connected to the default process.
        '''
        if self.__default is None:
            self.__default = self.Process("Default")
        return self.__default


    def __getitem__(self,key):
        return self.__dict__[key]


import autest.api
from autest.core.test import Test
from autest.core.testrun import TestRun
autest.api.AddTestEntityMember(Processes, classes=[Test, TestRun])

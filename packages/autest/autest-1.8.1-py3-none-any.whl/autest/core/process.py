from __future__ import absolute_import, division, print_function
from autest.common.constructor import call_base, smart_init
import hosts.output as host

from .runable import Runable
from .order import Order
from .item import Item
from . import setup

import os
from typing import List, Optional


@smart_init
class Process(Runable, Order, Item):
    __slots__: List[str] = []

    @call_base(Runable=("runable",), Order=(), Item=(None, "name"))
    def __init__(self, runable, name, cmdstr=None, use_shell=None):

        self.__cmdstr = cmdstr
        self.__use_shell = use_shell
        self.__streams = object()

        self.__output = os.path.join(
            self._RootRunable.RunDirectory, "_output{0}{1}-{2}".format(
                os.sep,
                self._ParentRunable._ID,
                self._ID
            )
        )

        # will want to refactor setup later
        self.__setup = setup.Setup(self)

    @property
    def Setup(self):
        '''
        The setup object for this given process.
        See Setup for more information.
        '''
        return self.__setup

    @property
    def Name(self) -> str:
        '''
        The name or ID of the process

        :getter: returns the name
        '''
        return self._ID

    @property
    def StreamOutputDirectory(self) -> str:
        '''
        The path to the where all stream files will be written to

        '''
        return self.__output

    @property
    def Command(self) -> Optional[str]:
        '''
        The command used to start the process
        '''
        return self.__cmdstr

    @Command.setter
    def Command(self, value: str) -> None:
        value = value.replace('/', os.sep)
        self.__cmdstr = value

    # need to remember if this case is needed
    # ///////////////////////
    @property
    def RawCommand(self):
        return self.__cmdstr

    @RawCommand.setter
    def RawCommand(self, value):
        self.__cmdstr = value
    # ////////////////////////

    @property
    def ForceUseShell(self) -> bool:
        '''
        Forces the use of a shell when running the command.
        Normally AuTest will try to detect if there shell related commands or syntax in the command
        and will only spawn a shell in those cases.
        However in certain cases it fails to get this correct and need to be explicitly told to use the shell
        '''
        return self.__use_shell

    @ForceUseShell.setter
    def ForceUseShell(self, val):
        self.__use_shell = bool(val)

    @property
    def StartupTimeout(self) -> float:
        '''
        This is the value of how long AuTest will wait for the given process to start
        and be considered ready before it will stop the process and report an error.
        Set this value to allow for more or less time.
        '''
        return self.__startup_timeout

    @StartupTimeout.setter
    def StartupTimeout(self, val: float):
        self.__startup_timeout = float(val)

    @property
    def _ChildRunables(self):
        return self.Setup._Items

    @property
    def TestDirectory(self) -> str:
        '''
        Returns the directory where the test file exists
        '''
        return self._RootRunable.TestDirectory

    @property
    def TestFile(self) -> str:
        '''
        Returns the name of the test file that defines this test
        '''
        return self._RootRunable.TestFile

    @property
    def TestRoot(self) -> str:
        '''
        Returns the root directory in which autest start scanning for tests
        '''
        return self._RootRunable.TestRoot

    @property
    def RunDirectory(self) -> str:
        '''
        Returns the directory this test will run in.
        This maps to a directory under the sandbox root directory.
        '''
        return self._RootRunable.RunDirectory

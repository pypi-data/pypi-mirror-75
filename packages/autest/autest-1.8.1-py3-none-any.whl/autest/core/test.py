from __future__ import absolute_import, division, print_function

import os
import copy


import autest.testers as testers
import autest.glb as glb
import hosts.output as host

from .runable import Runable
from .order import Order
from .item import Item
from autest.common.constructor import call_base, smart_init
from autest.common.execfile import execFile
from autest.core.testerset import TesterSet
from . import setup
from . import conditions
from . import testrun
from . import CopyLogic


@smart_init
class Test(Runable, Order, Item):
    __slots__ = ["__run_serial",
                 "__setup",
                 "__test_runs",
                 "__test_dir",
                 "__test_file",
                 "__test_root",
                 "__run_dir",
                 "__result",
                 "__processes",
                 "__conditions", ]

    @call_base(Runable=(None,), Order=(), Item=(None, "id"))
    def __init__(self, id, test_dir, test_file, run_root, test_root, env, variables):

        # additional variables
        self.Variables = variables

        self.__run_serial = False

        # internal data
        # the different test runs
        self.__test_runs = []
        # this is the location of the test file
        self.__test_dir = test_dir
        # this is the name of the test file
        self.__test_file = test_file
        # this is the directory we scanned to find this test
        self.__test_root = test_root
        # this is the directory we will run the test in
        self.__run_dir = os.path.normpath(os.path.join(run_root, id))
        # this is the result of the test ( did it pass, fail, etc...)
        self.__result = None
        # controls is we should continue on a failure
        self.__continueonfail = False

        # this is a bit of a hack as this hard coded in..  try to address later
        # this is the set of extra processes that we might need running
        # for the test to work
        # self.__processes=Processes(self)

        # property objects
        self.__setup = setup.Setup(self)
        self.__conditions = conditions.Conditions()

        # make a copy of the environment so we can modify it without issue
        self.Env = env
        # add some default values
        self.Env['AUTEST_TEST_ROOT_DIR'] = self.__test_root
        self.Env['AUTEST_TEST_DIR'] = self.__test_dir
        self.Env['AUTEST_RUN_DIR'] = self.__run_dir

        # TimeOut
        self._Register(
            "Test.{0}.TimeOut".format(self.Name),
            TesterSet(
                testers.LessThan,
                "TotalRunTime",
                self.RunningEvent,
                converter=float,
                kill_on_failure=True,
                description_group="Time-Out",
                description="Test finishes within expected time"),
            "TimeOut")

        timeout = self.Variables.Autest.Test.TimeOut

        if timeout is not None:
            self.TimeOut = timeout

# public properties
    @property
    def Name(self):
        '''
        The name of the test

        :getter: Returns the name.
        '''
        return self._ID

    @Name.setter
    def Name(self, val: str):
        self._ID = val

    @property
    def Summary(self) -> str:
        '''
        Summary of what this test is about and or does.

        Examples:

            .. code::

                Test.Summary="Test the loading of config file"
        '''

        return self._Description

    @Summary.setter
    def Summary(self, val: str):
        self._Description = val

    @property
    def RunSerial(self) -> bool:
        '''
        A Boolean value of True or False.
        Stated that this test has to run be itself in serially without any other tests running.
        This prevents cases in which the test, for whatever reason, cannot run in parallel with another test.
        By default, this value is False.
        It only has effect if the --jobs option is greater than 1
        '''
        return self.__run_serial

    @RunSerial.setter
    def RunSerial(self, val: bool):
        self.__run_serial = val

    @property
    def Setup(self) -> setup.Setup:
        '''
            The setup object for this given process.
            See Setup for more information.
        '''
        return self.__setup

    def SkipIf(self, *lst):
        '''
        This method takes one or more conditions as defined by the condition namespace.
        If any of the conditions are true, the test will be skipped

        :arg *lst: condition(s) to check to determine if a test should be skipped.

        Examples:

            Skip test if platform is not Windows

            .. code:: python

                Test.SkipIf(Condition.IsNotPlatform('windows'))
        '''
        return self.__conditions._AddConditionIf(lst)

    def SkipUnless(self, *lst):
        '''
        This method takes one or more conditions as defined by the condition namespace.
        If any of the conditions are false, the test will be skipped

        :arg *lst: condition to test if a test should be skipped.

        Examples:

            Run test if and only if gcc exists and the platform is a POSIX or windows

            .. sourcecode:: python

                Test.SkipUnless(
                Condition.HasProgram(
                    "gcc"
                ),
                Condition.IsPlatform('posix','windows')
                )
        '''
        return self.__conditions._AddConditionUnless(lst)

    @property
    def TestDirectory(self):
        '''
        Returns the directory where the test file exists
        '''
        return self.__test_dir

    @property
    def TestFile(self):
        '''
        Returns the name of the test file that defines this test
        '''
        return self.__test_file

    @property
    def TestRoot(self):
        '''
        Returns the root directory in which autest start scanning for tests
        '''
        return self.__test_root

    @property
    def RunDirectory(self):
        '''
        Returns the directory this test will run in.
        This maps to a directory under the sandbox root directory.
        '''
        return self.__run_dir

    # public methods
    def AddTestRun(self, displaystr=None, name='tr',):
        '''
        Creates a new TestRun object.
        The order in which these are created controls the order in which they run.

        :arg str displaystr:
            A description of what the test run does.
            Used in the reports to help clarify what is happening
            If not defined a general auto generated value will be used based on the name property

        :arg str name:
            The name of the test run.
            The provided value will be appended with a value of "-{num of test runs so far}"
            Used to define locations on disk under the sandbox.
            Useful to help define what a given test run maybe doing.
            If not defined a default value of "tr" will be used.

        '''
        tmp = testrun.TestRun(self, "{0}-{1}".format(len(self._TestRuns), name), displaystr)
        self._TestRuns.append(tmp)
        return tmp

    # internal stuff

    @property
    def _TestRuns(self):
        return self.__test_runs

    @property
    def _Conditions(self):
        return self.__conditions

    @property
    def _ChildRunables(self):
        return self.Setup._Items + list(self.Processes._Items) + self.__test_runs

    @property
    def ContinueOnFail(self) -> bool:
        '''
        Controls if the test should continue running if this test run does not pass.
        Can be set to True or False.
        '''
        return self.__continueonfail

    @ContinueOnFail.setter
    def ContinueOnFail(self, val):
        self.__continueonfail = val


def loadTest(test):
    # load the test data.  this mean exec the data
    # create the locals we want to pass
    locals = copy.copy(glb.Locals)

    locals.update({
        'test': test,  # backwards compat
        'Test': test,
        'Setup': test.Setup,
        'Condition': conditions.ConditionFactory(test.ComposeVariables(), test.ComposeEnv()),
        'Testers': testers,
        # break these out of tester space
        # to make it easier to right a test
        'Any': testers.Any,
        'All': testers.All,
        'Not': testers.Not,
        'When': glb.When(),
        'CopyLogic': CopyLogic,
    })

    # get full path
    fileName = os.path.join(test.TestDirectory,
                            test.TestFile)
    host.WriteVerbose(["test_logic", "reading"],
                      'reading test "{0}"'.format(test.Name))
    execFile(fileName, locals, locals)
    host.WriteVerbose(["test_logic", "reading"],
                      'Done reading test "{0}"'.format(test.Name))

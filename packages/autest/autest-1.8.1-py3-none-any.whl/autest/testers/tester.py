
import abc
import os.path
import traceback
from enum import IntEnum
from typing import Any, Optional

import colorama

import autest.core.eventinfo
from autest.exceptions.killonfailure import KillOnFailureError


def get_name(obj):
    if hasattr(obj, '__call__'):
        return "{0} {1}".format(obj.__self__.Name, obj.__name__)
    return obj


class ResultType(IntEnum):
    Unknown = 0
    Skipped = 1
    Passed = 2
    Warning = 3
    Failed = 4
    Exception = 5

    # TODO dynamically generate this?
    # @classmethod
    # def to_list():
    #     return ["Unknown", "Skipped", "Passed", "Warning", "Failed", "Exception"]

    @classmethod
    def to_string(cls, result: int):
        for name, value in vars(cls).items():
            if value == result:
                return name
        return "Unknown"

    @classmethod
    def to_color_string(cls, result: int):
        '''
        Turns a the provided ResultType in to a string with color codes.

        Args:
            result: the result type value

        '''
        c = colorama.Style.BRIGHT
        if ResultType.Unknown == result:
            c = colorama.Style.BRIGHT
        elif ResultType.Passed == result:
            c = colorama.Fore.GREEN
        elif ResultType.Skipped == result:
            c = colorama.Style.BRIGHT
        elif ResultType.Warning == result:
            c = colorama.Fore.YELLOW
        elif ResultType.Failed == result:
            c = colorama.Fore.RED
        elif ResultType.Exception == result:
            c = colorama.Fore.RED

        ResultType.to_string(result)

        return colorama.Style.RESET_ALL + c + ResultType.to_string(result) + "{{host.reset-stream}}"


class Tester(object):
    '''
    The base tester object contains the basic properties all testers should fill in

    Args:
        value:
            The value we are testing for

        test_value:
            The runtime value we will test.
            This is normally a string that is used to reference the eventinfo object for a runtime value.
            However it might be a user defined value, such as a path to a file.
            It can also be a function that will be called to return the expected content to test against.

        kill_on_failure:
            Setting this to True will kill the test from processing the rest of the test run and any existing item
            in the event queue for the current scope.
            This should only be used in cases when a failure mean we really need to do a hard stop.
            For example need to stop because the test ran to long.

        description_group:
            This is extra information about the file, process, etc that might be useful to give the test more context,
            should be in form of 'Type: name', ie 'Process: proc1'

        description:
            This is what we are testing such as "Testing return code is 5" or "Checking file file X exists"

        result:
            This returns a ResultType object telling us how to process the result of the test

        bind:
            Internal argument used pass the internal Runable object being tested.

    '''

    def __init__(self,
                 value: Any,
                 test_value: Any,
                 kill_on_failure: bool = False,
                 description_group: Optional[str] = None,
                 description: Optional[str] = None,
                 bind=None):

        self._description_group: Optional[str] = description_group
        self._description: Optional[str] = description
        self.__result = ResultType.Unknown
        self.__reason = "Test was not run"
        self._test_value = test_value
        self.__kill: bool = kill_on_failure
        self.__value = value
        self.__ran = False
        self._bind = bind

    @property
    def KillOnFailure(self) -> bool:
        '''
        If this is set to True we want to stop that main process
        from running
        '''
        return self.__kill

    @KillOnFailure.setter
    def KillOnFailure(self, value: bool) -> None:
        self.__kill = value

    @property
    def Bind(self):
        '''
        This is the Bind events function. Use this function to call
        Test Directory.
        '''
        return self._bind

    @Bind.setter
    def Bind(self, value) -> None:
        self._bind = value

    @property
    def TestValue(self) -> Any:
        '''
        This is the runtime value we want to test against. This
        attribute will return the value in question or a function
        that can get this value for us.
        '''
        return self._test_value

    @TestValue.setter
    def TestValue(self, value: Any):
        self._test_value = value

    @property
    def Value(self) -> Any:
        '''
        This is the "static" value to test for based on what was set
        in the test file.
        '''
        return self.__value

    @Value.setter
    def Value(self, val: Any) -> None:
        self.__value = val

    @property
    def Description(self) -> str:
        '''
        description of what is being tested
        '''
        return self._description

    @Description.setter
    def Description(self, val: str) -> None:
        self._description = val

    @property
    def DescriptionGroup(self) -> str:
        '''
        description of what is being tested
        '''
        return self._description_group

    @DescriptionGroup.setter
    def DescriptionGroup(self, val: str):
        self._description_group = val

    @property
    def Reason(self) -> str:
        '''
        This is a string (possibly multiline) with information about why the result happened.
        This maybe as simple as "Return code equal to 5" or it might be more complex with diffs of what was different in a text file
        '''
        return self.__reason

    @Reason.setter
    def Reason(self, val: str) -> None:
        self.__reason = val

    @property
    def Result(self) -> ResultType:
        '''
        The result of the test
        '''
        return self.__result

    @Result.setter
    def Result(self, val: ResultType) -> None:
        '''
        Sets the result of a test
        '''
        self.__result = val

    def __call__(self, eventinfo, **kw):
        '''
        Calls the test function and handles the common error cases
        '''
        try:
            self.__ran = True
            self.test(eventinfo, **kw)
        except KeyboardInterrupt:
            raise
        except KillOnFailureError:
            raise
        except Exception:
            self.Result = ResultType.Exception
            self.Reason = traceback.format_exc()

    @abc.abstractmethod
    def test(self, eventinfo, **kw):
        '''
        This is called to test a given event
        it should store the result of the test in the Result property
        and set the message of why the test failed to the ResultData property
        The return value is ignored
        '''
        return

    def GetContent(self, eventinfo, test_value=None):
        return self._GetContent(eventinfo, test_value)

    def _GetContent(self, eventinfo, test_value=None):
        '''
        This is the magic function that makes goal is to provide the
        content needed for the test to happen in a generic way.
        '''
        # if test_value is None
        # we set it to the this testers object
        # test value.

        if test_value is None:
            test_value = self.TestValue

        # start off by trying to call this as an object
        # that now how to get content off the event info
        # object.
        try:
            ret, msg = test_value.GetContent(eventinfo)
            if ret is None:
                self.Result = ResultType.Failed
                self.Reason = msg
                return None
            return ret
        except AttributeError:
            pass
        # if that did not work because GetContent() does not exist
        # try to call object as a function (ie callable) that takes
        # that takes an eventinfo object
        try:
            ret, msg = test_value(eventinfo)
            if ret is None:
                self.Result = ResultType.Failed
                self.Reason = msg
                return None
            return ret
        except TypeError:
            pass
        # if that did not work see if this
        # is a string.  If so we assume it an attribute of the event.
        # It is filename of test file otherwise.

        if isinstance(test_value, str):
            if hasattr(eventinfo, test_value):
                return getattr(eventinfo, test_value)
            else:
                return os.path.join(self._bind._Runable.TestDirectory, test_value)

        # if that failed, we see if this has a __call__ attribute
        # in this case we know we can call it as a function.
        # we assume that it accepts no arguments as we would not know
        # what to pass it.
        try:
            if hasattr(test_value, '__call__'):
                return test_value()
        except AttributeError:
            pass
        # this is the else
        # we give up and assume it the value we want to pass in
        return test_value

    @property
    def UseInReport(self) -> bool:
        return True

    @property
    def RanOnce(self) -> bool:
        return self.__ran

    @property
    def isContainer(self) -> bool:
        return False

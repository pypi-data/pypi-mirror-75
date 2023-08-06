from typing import Optional

import hosts.output as host
from autest.exceptions.killonfailure import KillOnFailureError

from . import tester


class _Container(tester.Tester):

    def __init__(self, *lst, **kw):
        self.__testers = lst
        super(_Container, self).__init__(None, None, **kw)

    def _verify(self, converter):
        tmp = []
        for i in self._testers:
            if isinstance(i, _Container):
                i._verify(converter)
                tmp.append(i)
            elif isinstance(i, tester.Tester):
                tmp.append(i)
            else:
                tmp.append(converter(i))
        self.__testers = tmp

    @property
    def _testers(self):
        return self.__testers

    @property
    def isContainer(self):
        return True

    @property
    def TestValue(self):
        '''
        This is the runtime value we want to test against. This
        attribute will return the value in question or a function
        that can get this value for us.
        '''
        return self._test_value

    @TestValue.setter
    def TestValue(self, value):
        self._test_value = value
        for t in self._testers:
            t.TestValue = self._test_value

    #@property
    # def KillOnFailure( self ):
    #    return self.__kill

    #@KillOnFailure.setter
    # def KillOnFailure( self, value ):
    #    self.__kill = value

    @property
    def Description(self):
        '''
        description of what is being tested
        '''
        return self._description

    @Description.setter
    def Description(self, val):
        self._description = val
        for t in self._testers:
            t.Description = self._description

    @property
    def DescriptionGroup(self):
        '''
        description of what is being tested
        '''
        return self._description_group

    @DescriptionGroup.setter
    def DescriptionGroup(self, val):
        self._description_group = val
        for t in self._testers:
            t.DescriptionGroup = self._description_group


class Any(_Container):
    '''
    Passes if any of the provided Tester passes.
    Provided in as a Global to help with ease of use.

    Args:
        *lst:
            The function list of all Testers provided

    Example:

        Test is the return code is 0 or 5

        .. code:: python3

            tr.Processes.Default.ReturnCode = Any(0,5)


        Test that the stdout stream of process match one of two possible gold files

        .. code:: python3

            tr.Processes.Default.Streams.stdin = All("gold/hello1.gold", "gold/hello2.gold")

    '''

    def __init__(self, *lst):
        super(Any, self).__init__(
            *lst, description="Checking that any test passes")

    def test(self, eventinfo, **kw):
        for t in self._testers:
            t.test(eventinfo, **kw)
            if t.Result == tester.ResultType.Passed:
                self.Result = tester.ResultType.Passed

        # self.Result may be set to Unknown if none of the testers passed
        if self.Result == tester.ResultType.Unknown:
            self.Result = tester.ResultType.Failed
            self.Reason = "None of the tests passed"

        if self.Result == tester.ResultType.Passed:
            self.Reason = "One or more tests passed"
        else:
            self.Reason = "None of the tests passed"


class All(_Container):
    '''
    Passes if all of the provided Tester pass.
    This can also be achieved in many cases by just using the `+=` operator on the testable property.
    Provided in as a Global to help with ease of use.

    Args:
        *lst:
            The function list of all Testers provided

    Example:

        Test is the File object

        .. code:: python3

            f = Test.Disk.File("foo.txt")
            f.Content = All(
                            Testers.ContainsExpression("value1", 'Has value1')
                            Testers.ContainsExpression("value2", 'Has value2')
                            )
            # this is the same as saying...
            f.Content = Testers.ContainsExpression("value1", 'Has value1')
            f.Content += Testers.ContainsExpression("value2", 'Has value2')


        Test that the stdout stream of process match a gold files and does not contain an expression.
        In this case the gold file might have a wild card for a data section, which normally can be ignored,
        unless it contains a certain values.

        .. code:: python3

            tr.Processes.Default.Streams.stdin = All(
                "gold/hello1.gold",
                Testers.ExcludesExpression("bad value", "Does not contain 'bad value'")
                )
    '''

    def __init__(self, *lst):
        super(All, self).__init__(
            *lst, description="Checking that all tests pass")

    def test(self, eventinfo, **kw):
        for t in self._testers:
            t.test(eventinfo, **kw)
            if t.Result == tester.ResultType.Failed:
                self.Result = tester.ResultType.Failed
        if self.Result != tester.ResultType.Failed:
            self.Result = tester.ResultType.Passed

        if self.Result == tester.ResultType.Passed:
            self.Reason = "All the tests passed"
        else:
            self.Reason = "One or more tests did not pass"


class Not(_Container):
    '''
    Results in the negation of the Test as passing.
    The Python not operator `!` cannot be used as it results in immediate result.
    This allows for a delay result needed for composing more complex tester logic.
    Provided in as a Global to help with ease of use.

    Example:

        Test is the return code is a non-zero value

        .. code:: python3

            tr.Processes.Default.ReturnCode = Not(0)

    '''

    def __init__(self, testobj):
        super(Not, self).__init__(
            testobj, description="Checking that negation of the test")

    def test(self, eventinfo, **kw):
        t = self._testers[0]
        try:
            t.test(eventinfo, **kw)
        except KillOnFailureError:
            self.Result = tester.ResultType.Passed
            self.Reason = "The test contained test failed as expected"
            raise
        if t.Result == tester.ResultType.Failed:
            self.Result = tester.ResultType.Passed
            self.Reason = "The test contained test failed as expected"
        # if Warning is clarified better, we might want it to be an error as
        # well
        elif t.Result == tester.ResultType.Passed:
            self.Reason = "The test contained test passed when it was expected to fail"
            self.Result = tester.ResultType.Failed

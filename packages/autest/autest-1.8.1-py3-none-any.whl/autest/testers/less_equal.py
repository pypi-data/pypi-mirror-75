from typing import Any, Optional

import hosts.output as host
from autest.exceptions.killonfailure import KillOnFailureError

from . import tester


class LessEqual(tester.Tester):
    '''
    Test that the value is less than or equal to the expected value.

    Args:
        value:
            The value we are testing for

        test_value:
            The runtime value we will test.
            This is normally a string that is used to reference the eventinfo object for a runtime value.
            However it might be a user defined value, such as a path to a file.
            It can also be a function that will be called to return the expected content to test against.

        kill_on_failure:
            Setting this to True will kill the test from processing the rest of the test run and any existing item in the event
            queue for the current scope.
            This should only be used in cases when a failure mean we really need to do a hard stop.
            For example need to stop because the test ran to long.

        description_group:
            This is extra information about the file, process, etc that might be useful to give the test more context, should be
            in form of 'Type: name', ie 'Process: proc1'

        description:
            This is what we are testing such as "Testing return code is 5" or "Checking file file X exists"

    '''

    def __init__(
            self,
            value: Any,
            test_value=None,
            kill_on_failure: bool = False,
            description_group: Optional[str] = None,
            description: Optional[str] = None):

        if description is None:
            description = "Checking that {0} <= {1}"
        super(LessEqual, self).__init__(
            value=value,
            test_value=test_value,
            kill_on_failure=kill_on_failure,
            description_group=description_group,
            description=description)

    def test(self, eventinfo, **kw):
        # Get value to test against
        val = self._GetContent(eventinfo)
        self.Description = self.Description.format(
            tester.get_name(self.TestValue), self.Value, ev=eventinfo)
        # do test
        if val > self.Value:
            self.Result = tester.ResultType.Failed
            if self.DescriptionGroup:
                self.DescriptionGroup.format(eval=eventinfo)
            reason = "Returned value: {0} > {1}".format(val, self.Value)
            self.Reason = reason
            if self.KillOnFailure:
                raise KillOnFailureError
        else:
            self.Result = tester.ResultType.Passed
            self.Reason = "Returned value: {0} <= {1}".format(val, self.Value)
        host.WriteVerbose(
            ["testers.LessEqual", "testers"],
            "{0} - ".format(tester.ResultType.to_color_string(self.Result)),
            self.Reason)

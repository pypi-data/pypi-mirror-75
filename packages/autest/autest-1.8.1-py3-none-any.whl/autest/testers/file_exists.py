import os
from typing import Optional

import hosts.output as host

from . import tester


class FileExists(tester.Tester):
    '''
    Test that the file exists or does not exist on Disk.

    Args:
        exists:
            Test that is the file exists if True, else non-existence.

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


    '''

    def __init__(
            self,
            exists: bool,
            test_value: Optional[str] = None,
            kill_on_failure: bool = False,
            description_group: Optional[str] = None,
            description: Optional[str] = None
        ):

        if description is None:
            if exists:
                description = 'Checking that file "{0}" exists'.format(
                    tester.get_name(test_value))
            else:
                description = 'Checking that file "{0}" does not exists'.format(
                    tester.get_name(test_value))
        super(FileExists, self).__init__(value=exists,
                                         test_value=test_value,
                                         kill_on_failure=kill_on_failure,
                                         description_group=description_group,
                                         description=description)

    def test(self, eventinfo, **kw):
        filename = self._GetContent(eventinfo)
        if os.path.isfile(filename):
            if self.Value:
                self.Result = tester.ResultType.Passed
                self.Reason = 'File "{0}" exists'.format(self.TestValue)
            else:
                self.Result = tester.ResultType.Failed
                self.Reason = 'File "{0}" exists and it should not'.format(
                    self.TestValue)
        else:
            if self.Value:
                self.Result = tester.ResultType.Failed
                self.Reason = 'File "{0}" does not exists and it should'.format(
                    self.TestValue)
            else:
                self.Result = tester.ResultType.Passed
                self.Reason = 'File "{0}" does not exists'.format(
                    self.TestValue)
        host.WriteVerbose(["testers.FileExists", "testers"], "{0} - ".format(
            tester.ResultType.to_color_string(self.Result)), self.Reason)

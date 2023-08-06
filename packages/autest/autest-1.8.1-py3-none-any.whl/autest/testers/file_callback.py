from typing import Optional

import hosts.output as host
from autest.exceptions.killonfailure import KillOnFailureError

from . import tester


class FileContentCallback(tester.Tester):
    '''
    Allow for defining custom content tests for a file or stream object

    Args:
        callback:
            The callback function.
        test_value:
            The runtime value we will test.
            This is normally a string that is used to reference the eventinfo object for a runtime value.
            However it might be a user defined value, such as a path to a file.
            It can also be a function that will be called to return the expected content to test against.

        description:
            This is what we are testing such as "Testing return code is 5" or "Checking file file X exists"

        kill_on_failure:
            Setting this to True will kill the test from processing the rest of the test run and any existing item
            in the event queue for the current scope.
            This should only be used in cases when a failure mean we really need to do a hard stop.
            For example need to stop because the test ran to long.

        description_group:
            This is extra information about the file, process, etc that might be useful to give the test more context,
            should be in form of 'Type: name', ie 'Process: proc1'

    Callback Interface:

    .. code::

        def callback(data:str) -> Optional[str]:
            return errorMessage

    **data**: is file contents

    **returns**: either a string describing what's wrong with the test if it fails or
    '' or None if the test succeed.


    '''

    def __init__(self, callback, description, killOnFailure=False, description_group=None):
        super(FileContentCallback, self).__init__(value=callback,
                                                  test_value=None,  # set when it add the the tester member, should be a filename
                                                  kill_on_failure=killOnFailure,
                                                  description_group=description_group,
                                                  description=description)

    def test(self, eventinfo, **kw):
        filename = self._GetContent(eventinfo)
        if filename is None:
            filename = self.TestValue.AbsPath
        result = tester.ResultType.Passed
        try:
            with open(filename, 'r') as inp:
                data = inp.read()
        except IOError as err:
            result = tester.ResultType.Failed
            self.Reason = 'Cannot read {0}: {1}'.format(filename, err)
        else:
            # call the callback ( as it is Value)
            errorMessage = self.Value(data)
            if errorMessage:
                result = tester.ResultType.Failed
                self.Reason = 'Contents of {0} do not match desired callback: {1}'.\
                              format(filename, errorMessage)

        self.Result = result
        if result != tester.ResultType.Passed:
            if self.KillOnFailure:
                raise KillOnFailureError
        else:
            self.Reason = 'Contents of {0} match desired callback'.format(
                filename)
        host.WriteVerbose(["testers.Equal", "FileContentCallback"], "{0} - ".format(
            tester.ResultType.to_color_string(self.Result)), self.Reason)


from typing import Optional
import traceback

import hosts.output as host
from autest.exceptions.killonfailure import KillOnFailureError

from . import tester


class Lambda(tester.Tester):
    '''
    Allow providing to python function to:
        #. Provide a custom test
        #. Custom logic to execute as part of an AuTest event object being called.

    Args:
        func: The callback function to call
        kill_on_failure:
            Setting this to True will kill the test from processing the rest of the test run and any existing
            item in the event queue for the current scope.
            This should only be used in cases when a failure mean we really need to do a hard stop.
            For example need to stop because the test ran to long.

        description_group:
            This is extra information about the file, process, etc that might be useful to give the test more context,
            should be in form of 'Type: name', ie 'Process: proc1'



    Callback Interface:

        callback(eventinfo)

        callback(eventinfo,tester)

    Where:

        **eventinfo**: Object related to the event or test property the tester is mapped to.

        **tester**: Reference to the Lambda object. Can be used for better control setting state.

    The callback is expected to return a tuple of `(result:resulttype, description:str, message:str)` where:

        **resulttype**: is the ????

        **description**: A string describing what the Lambda is testing

        **message**: A string describing the result of the test.

    Example:
        This can also be use to help with advance Flow control by reacting to the eventinfo object.

        .. code::

            def StopProcess(event,time):
                if event.TotalRunTime > time:
                    event.object.Stop()
                return 0, "this is a test", "this is what happened"


            t = Test.AddTestRun()
            # Maps call back to the Running Event
            # This will stop the test in after it run for at least 1 second.
            t.RunningEvent.Connect(
                Testers.Lambda(
                    lambda ev: StopProcess(ev,1)
                )
            )

        Define a custom test.

        .. code::

            t = Test.AddTestRun("Get data of Python version")
            t.Processes.Default.Command = "python --version"
            t.ReturnCode = 0

            path = t.Processes.Default.Streams.All.AbsPath


            def custom_test(event, tester):
                with open(path) as f:
                    data1 = f.read()
                with open(tester.GetContent(event)) as f:
                    data2 = f.read()
                if data1 == data2:
                    return (True, "Check that versions match", "Python versions did matched")
                else:
                    return (False, "Check that versions match", "Python versions did not matched")


            t = Test.AddTestRun("Do it again")
            t.Processes.Default.Command = "python --version"
            t.ReturnCode = 0
            t.Processes.Default.Streams.All.Content = Testers.Lambda(custom_test)



    '''

    def __init__(self, func, kill_on_failure=False, description_group=None):
        super(Lambda, self).__init__(
            value=func,
            test_value=None,
            kill_on_failure=kill_on_failure,
            description_group=description_group)

    def test(self, eventinfo, **kw):
        # run the test function
        try:
            try:
                result, desc, message = self.Value(eventinfo, self)
            except TypeError:
                result, desc, message = self.Value(eventinfo)
        except Exception:
            result, desc, message = (False, "Exception was caught!",
                                     traceback.format_exc())
            self.KillOnFailure = True
        self.Description = desc
        self.Reason = message

        # process results
        if not result:
            self.Result = tester.ResultType.Failed
            host.WriteVerbose(["testers.Lambda", "testers"], "{0} - ".format(
                tester.ResultType.to_color_string(self.Result)), self.Reason)
            if self.KillOnFailure:
                raise KillOnFailureError(message)
        else:
            self.Result = tester.ResultType.Passed
        host.WriteVerbose(
            ["testers.Lambda", "testers"],
            "{0} - ".format(tester.ResultType.to_color_string(self.Result)),
            self.Reason)

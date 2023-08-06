import re
from typing import Optional

import hosts.output as host
from autest.exceptions.killonfailure import KillOnFailureError

from . import tester



class ExcludesExpression(tester.Tester):
    '''
    Test that the content does not contain the provided expression.

    If re.M is provided as part of the reflags argument the whole string will be tested with re.search.
    If re.M is not provided the content will be broken up into separate line and the expression is tested
    on each line with re.search.

    Args:
        regexp:
            The expression to test for.
        reflags:
            Optional set of re flags to control behavior of the expression.
        kill_on_failure:
            Setting this to True will kill the test from processing the rest of the test run and any existing
            item in the event queue for the current scope.
            This should only be used in cases when a failure mean we really need to do a hard stop.
            For example need to stop because the test ran to long.
        description_group:
            This is extra information about the file, process, etc that might be useful to give the test more context,
            should be in form of 'Type: name', ie 'Process: proc1'.
        description:
            This is what we are testing such as "Testing return code is 5" or "Checking file file X exists".


    '''

    def __init__(self, regexp, description, killOnFailure=False, description_group=None, reflags=0):
        if isinstance(regexp, str):
            if reflags:
                regexp = re.compile(regexp, reflags)
            else:
                regexp = re.compile(regexp)
        self._multiline = regexp.flags & re.M

        super(ExcludesExpression, self).__init__(
            value=regexp,
            test_value=None,
            kill_on_failure=killOnFailure,
            description_group=description_group,
            description=description
        )

    def test(self, eventinfo, **kw):
        filename = self._GetContent(eventinfo)
        if filename is None:
            filename = self.TestValue.AbsPath
        result = tester.ResultType.Passed
        try:
            failed = False
            details = []
            # if this is multi-line check
            if self._multiline:
                with open(filename, 'r') as infile:
                    data = infile.read()
                failed = self.Value.search(data)
            else:
                # if this is single expression check each line till match
                with open(filename, 'r') as infile:
                    for cnt, l in enumerate(infile):
                        tmp = self.Value.search(l)
                        if tmp:
                            details += [(cnt + 1, l[:-1])]
                            failed = True
            if failed:
                result = tester.ResultType.Failed
                tmpstr = ""
                if details:
                    tmpstr = "\n  Details:\n"
                    for line, text in details:
                        tmpstr += "    {0} : {1}\n".format(text, line)

                self.Reason = 'Contents of {0} contains expression: "{1}"{2}'.\
                              format(filename, self.Value.pattern, tmpstr)

        except IOError as err:
            result = tester.ResultType.Failed
            self.Reason = 'Cannot read {0}: {1}'.format(filename, err)

        self.Result = result
        if result != tester.ResultType.Passed:
            if self.KillOnFailure:
                raise KillOnFailureError
        else:
            self.Reason = 'Contents of {0} excludes expression'.format(
                filename)
        host.WriteVerbose(["testers.ExcludesExpression", "testers"], "{0} - ".format(
            tester.ResultType.to_color_string(self.Result)), self.Reason)

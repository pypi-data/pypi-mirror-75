import difflib
from typing import Optional

import hosts.output as host
from autest.exceptions.killonfailure import KillOnFailureError

from . import tester

g_escape = ['{}', '``']


def equalToEscape(val):
    if val in g_escape:
        return val
    return None


class GoldFile(tester.Tester):
    r'''
    Tests if a file matches expected results via comparing a file or stream output with the content of the gold file.
    The gold file can contain wild card statement of `{}` or `\`\`` to tell the testing logic that differences
    in the area are to be ignored.

    Args:
        goldfile: the gold file to be used for the test. Assumed to relative to the location of the test file.
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
        normalize_eol:
            If True will normalize the `\\\\r\\\\n` sequences to `\\\\n` to help with common differences between different
            operating system such as Unix or Windows systems. If False no normalizing will happen.
        description_group:
            This is extra information about the file, process, etc that might be useful to give the test more context,
            should be in form of 'Type: name', ie 'Process: proc1'
        description:
            This is what we are testing such as "Testing return code is 5" or "Checking file file X exists"


    Examples:

        Test a gold file with new normalization of new line of /r/n to /n

        .. code:: python

            tr.Processes.Default.stdout= Testers.GoldFile("gold/exists.gold", normalize_eol=True)

    '''

    def __init__(self,
                 goldfile: str,
                 test_value: Optional[str] = None,
                 kill_on_failure: bool = False,
                 normalize_eol: bool = True,
                 description_group: str = None,
                 description: Optional[str] = None):
        if description is None:
            description = "Checking that {0} matches {1}".format(test_value,
                                                                 goldfile)
        super(GoldFile, self).__init__(
            value=goldfile,
            test_value=test_value,
            kill_on_failure=kill_on_failure,
            description_group=description_group,
            description=description)

        self._goldfile = self.Value
        self._normalize_eol = normalize_eol
        self.__test_value = None

    def test(self, eventinfo, **kw):

        # get the attribute file context
        tmp = self._GetContent(eventinfo)

        if tmp is None:
            pass
        try:
            with open(tmp) as val_file:
                val_content = val_file.read()
        except (OSError, IOError) as e:
            self.Result = tester.ResultType.Failed
            self.Reason = str(e)
            return

        # get the gold file context
        tmp = self._GetContent(eventinfo, self._goldfile)
        if tmp is None:
            pass
        try:
            with open(tmp) as gf_file:
                gf_content = gf_file.read()
        except KeyboardInterrupt:
            raise
        except Exception as e:
            self.Result = tester.ResultType.Failed
            if tmp is None:
                self.Reason = "Internal error: Invalid filename value of None. Filename must be of type string"
            else:
                self.Reason = "Can't open file {0} because:\n {1}".format(tmp, e)
            host.WriteVerbose(["testers.GoldFile", "testers"], "{0} - ".format(
                tester.ResultType.to_color_string(self.Result)), self.Reason)
            return

        if self._normalize_eol:
            val_content = val_content.replace("\r\n", "\n")
            gf_content = gf_content.replace("\r\n", "\n")

        # make seqerncer differ
        seq = difflib.SequenceMatcher(
            None, val_content, gf_content, autojunk=False)
        # do we have a match
        if seq.ratio() == 1.0:
            # The says ratio everything matched
            self.Result = tester.ResultType.Passed
            self.Reason = "Values match"
            host.WriteVerbose(["testers.GoldFile", "testers"], "{0} - ".format(
                tester.ResultType.to_color_string(self.Result)), self.Reason)
            return
        # if we are here we don't have a match at the moment.  At this point we
        # process difference to see if they
        # match and special code we have and do replacements of values and diff
        # again to see if we have a match
        # get diffs
        results = seq.get_opcodes()
        newtext = ''
        sub = False  # true is we are doign a {} and have not had non-white space to replace
        for tag, i1, i2, j1, j2 in results:
            # technically we can see that we might have a real diff
            # but we continue as this allow certain values to be replaced
            # helping to make the
            # finial diff string more readable
            data = gf_content[j1:j2].strip()
            tmp = equalToEscape(data.strip())
            if tmp or (data == '' and sub is True):
                sub = True
                data = tmp if tmp else '``'
                if tag != 'insert':
                    tag = "replace"
            else:
                sub = False
            if tag == "replace":
                tmp = self._do_action_replace(data, val_content[i1:i2])
                if tmp:
                    newtext += tmp
                    continue

            if tag == "insert":
                tmp = self._do_action_add(data, val_content[i1:i2])
                if tmp is not None:
                    newtext += tmp
                    continue

            newtext += gf_content[j1:j2]

        # reset the sequence test
        seq.set_seq2(newtext)
        if seq.ratio() == 1.0:
            # The says ratio everything matched
            self.Result = tester.ResultType.Passed
            self.Reason = "Values match"
            host.WriteVerbose(["testers.GoldFile", "testers"], "{0} - ".format(
                tester.ResultType.to_color_string(self.Result)), self.Reason)
            return
        # this makes a nice string value..
        diff = difflib.Differ()
        self.Result = tester.ResultType.Failed

        tmp_result = "\n".join(
            diff.compare(newtext.splitlines(), val_content.splitlines()))

        self.Reason = "File differences\nGold File : {0}\nData File : {1}\n{2}".format(
            self._GetContent(eventinfo, self._goldfile),
            self._GetContent(eventinfo), tmp_result)
        host.WriteVerbose(
            ["testers.GoldFile", "testers"],
            "{0} - ".format(tester.ResultType.to_color_string(self.Result)),
            self.Reason)
        if self.KillOnFailure:
            raise KillOnFailureError

        # todo Change this logic to
        # replace gold file text token with special values
        # special value is key, while original text is the "action"
        # on first diff we see if replace text matches key, if so we do action
        # note unique key need to be a safe, ideally control character that
        # would not be typed
        # or added to a text file normally
    def _do_action_replace(self, data, text):
        try:
            if equalToEscape(data):
                return text
            # more options when we need them
            # elif data == "range":
            # pass
        except KeyError:
            # key are not found, so we assume we should default actions
            pass
        return None

    def _do_action_add(self, data, text):
        try:
            if equalToEscape(data.strip()):
                return ''
        except KeyError:
            pass
        return None


class GoldFileList(tester.Tester):
    def __init__(self,
                 goldfilesList,
                 test_value=None,
                 kill_on_failure=False,
                 normalize_eol=True,
                 description_group=None,
                 description=None):
        super(GoldFileList, self).__init__(
            test_value=test_value,
            kill_on_failure=kill_on_failure,
            description_group=description_group,
            description=description)
        self.Description = "Checking that {0} matches one of {1}".format(
            test_value, ', '.join([str(gold) for gold in goldfilesList]))
        golds = []
        for goldfile in goldfilesList:
            golds.append(
                GoldFile(
                    goldfile,
                    test_value=test_value,
                    kill_on_failure=kill_on_failure,
                    normalize_eol=normalize_eol))
        self._golds = golds

    def test(self, eventinfo, **kw):
        results = []
        for gold in self._golds:
            gold.test(eventinfo, **kw)
            results.append(gold.Reason)
            if gold.Result == tester.ResultType.Passed:
                self.Result = tester.ResultType.Passed
                self.Reason = 'Gold file %s matched' % gold._goldfile
                return

        # there were no matching gold files found
        self.Result = tester.ResultType.Failed
        self.Reason = 'No matching gold files found, differences:\n{0}'.format(
            '\n\n'.join(results))

    @property
    def TestValue(self):
        return self.__test_value

    @TestValue.setter
    def TestValue(self, value):
        self.__test_value = value
        for gold in self._golds:
            gold.TestValue = value

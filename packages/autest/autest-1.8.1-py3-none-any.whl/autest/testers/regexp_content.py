import re
from typing import Optional, Pattern

import hosts.output as host
from autest.exceptions.killonfailure import KillOnFailureError

from . import tester
from .file_callback import FileContentCallback

# this is around for backwards compatibility. Ideally this is not needed
# given the better ExcludeExpression and ContainExpression
# see if we can weed this one out....


class RegexpContent(FileContentCallback):
    '''
    Tests the content contains the provided regular expression.
    Uses re.search to test if an object exists or not.

    Args:
        regexp:
            a string or compiler regular expression object
        description:
            description of what is being tested for


    '''

    def __init__(self, regexp: Pattern, description: str, killOnFailure: bool = False, description_group: Optional[str] = None):
        if isinstance(regexp, str):
            regexp = re.compile(regexp)
        self.__regexp = regexp
        super(RegexpContent, self).__init__(self.__check,
                                            description, killOnFailure, description_group)

    def __check(self, data):
        if not self.__regexp.search(data):
            return 'Search of regular expression "{0}" failed to find match'.format(self.__regexp.pattern)

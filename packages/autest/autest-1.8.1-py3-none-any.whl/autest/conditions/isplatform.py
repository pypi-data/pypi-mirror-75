import sys
import os
import platform

import autest.api as api


def IsPlatform(self, *lst: str):
    '''
    Returns a condition that will resolve to True if one of the provided platform identifiers
    matches the value of python sys.platform, platform.system() or os.name.
    The string is tested in a case insensitive way. If a match is not found it will return False

    Args:
        *lst: function list of string values to test

    '''
    return self.Condition(
        lambda: sys.platform.lower() in lst or platform.system(
        ).lower() in lst or os.name.lower() in lst,
        'Platform must be one of {0}, reported value was "{1}" or "{2}"'.
        format(lst, platform.system().lower(), os.name),
        True,
        'Platform must not be one of {0}, reported value was "{1}" or "{2}"'.
        format(lst, platform.system().lower(), os.name),
    )


def IsNotPlatform(self, *lst: str):
    '''
    Returns a condition that will resolve to True if one of the provided platform identifiers
    does not matches the value of python sys.platform, platform.system() or os.name.
    The string is tested in a case insensitive way.
    If a match is found it will return False.

    Args:
        *lst: function list of string values to test

    '''

    return self.Condition(
        lambda: sys.platform.lower() in lst or platform.system(
        ).lower() in lst or os.name.lower() in lst,
        'Platform must not be one of {0}, reported value was "{1}" or "{2}"'.
        format(lst, platform.system().lower(), os.name),
        False,
        'Platform must be one of {0}, reported value was "{1}" or "{2}"'.
        format(lst, platform.system().lower(), os.name), )


api.ExtendCondition(IsPlatform)
api.ExtendCondition(IsNotPlatform)

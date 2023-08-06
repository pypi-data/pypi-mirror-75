import os
from typing import Union

import hosts.output as host
from autest.api import AddWhenFunction
from autest.testenities.file import File


def FileExists(file_path: Union[str, File]):
    '''
    Tests that a file exists on disk.

    Args:
        file_path: The path to the file to test

    '''
    if isinstance(file_path, File):    # file object
        file_path = file_path.AbsPath

    def file_exists(process, **kw):
        #pylint: disable=unused-argument
        fpath=file_path
        if not os.path.isabs(file_path):
            fpath = os.path.normpath(
                os.path.join(
                    process.RunDirectory,
                    file_path
                )
            )

        result = os.path.isfile(fpath)
        host.WriteDebug(
            ['FileExists', 'when'],
            "Testing for file to exist '{0}' : {1}".format(fpath, result)
        )
        return result

    return file_exists


def FileNotExists(file_path: Union[str, File]):
    '''
    Tests that a file not exists on disk.

    Args:
        file_path: The path to the file to test

    '''

    if isinstance(file_path, File):    # file object
        file_path = file_path.AbsPath

    def file_not_exists(process, **kw):
        #pylint: disable=unused-argument
        fpath=file_path
        if not os.path.isabs(file_path):
            fpath = os.path.normpath(
                os.path.join(
                    process.RunDirectory,
                    file_path
                )
            )

        result = not os.path.isfile(fpath)
        host.WriteDebug(
            ['FileNotExists', 'when'],
            "Test for file to not exist '{0}' : {1}".format(fpath, result)
        )
        return result

    return file_not_exists


def FileModified(file_path: Union[str, File]):
    '''
    Tests to see if the file has been modified.
    If the file does not exist, then it will test for existence of the file

    Args:
        file_path: The path to the file to test

    '''

    if isinstance(file_path, File):    # file object
        file_path = file_path.AbsPath

    state = {}

    def file_is_modified(process, **kw):
        #pylint: disable=unused-argument
        fpath=file_path
        host.WriteDebug(
            ['FileModified', 'when'],
            "working out of directory {0}".format(os.getcwd())
        )

        if not os.path.isabs(file_path):
            fpath = os.path.normpath(
                os.path.join(
                    process.RunDirectory,
                    file_path
                )
            )

        if os.path.isfile(fpath):
            current_mtime = os.path.getmtime(fpath)
        else:
            host.WriteDebug(["FileModified", "when"],
                            "file '{0}' does not exist yet".format(fpath))
            state["modify_time"] = 0
            return False

        if "modify_time" in state:
            host.WriteDebug(["FileModified", "when"],
                            "file was last modified at {0}".format(state["modify_time"]))
            return state["modify_time"] < current_mtime

        state["modify_time"] = current_mtime
        return False

    return file_is_modified


AddWhenFunction(FileExists, generator=True)
AddWhenFunction(FileNotExists, generator=True)
AddWhenFunction(FileModified, generator=True)


import os
from typing import Union
from autest.api import AddWhenFunction
from autest.testenities.directory import Directory
import hosts.output as host


def DirectoryExists(directory_path: Union[str, Directory]):
    '''
    Tests to see if the directory has exists.

    Args:
        directory_path: The path to the directory to test

    '''
    if isinstance(directory_path, Directory):    # directory object
        directory_path = directory_path.AbsPath

    def directory_exists(process, **kw):
        #pylint: disable=unused-argument
        if not os.path.isabs(directory_path):
            directory_path = os.path.normpath(
                os.path.join(
                    process.RunDirectory,
                    directory_path
                )
            )

        result = os.path.isdir(directory_path)
        host.WriteDebug(
            ['DirectoryExists', 'when'],
            "Testing for directory to exist '{0}' : {1}".format(directory_path, result)
        )
        return result

    return directory_exists


def DirectoryNotExists(directory_path: Union[str, Directory]):
    '''
    Tests to see if the directory does not exist.

    Args:
        directory_path: The path to the directory to test

    '''
    if isinstance(directory_path, Directory):    # directory object
        directory_path = directory_path.AbsPath

    def directory_not_exists(process, **kw):
        #pylint: disable=unused-argument

        if not os.path.isabs(directory_path):
            directory_path = os.path.normpath(
                os.path.join(
                    process.RunDirectory,
                    directory_path
                )
            )

        result = not os.path.isdir(directory_path)
        host.WriteDebug(
            ['DirectoryNotExists', 'when'],
            "Test for directory to not exist '{0}' : {1}".format(directory_path, result)
        )
        return result

    return directory_not_exists


# todo add tests for removal
# todo add logic to do a recursive check?
def DirectoryModified(directory_path: Union[str, Directory]):
    '''
    Tests to see if the directory has been modified.
    The change is done via checking for a time stamp difference.
    On most operating systems this only changes when a file or directory was added,
    or removed in that directory, not and subdirectories below it.
    If the directory does not exist, then it will test for existence of the directory

    Args:
        file_path: The path to the file to test

    '''
    if isinstance(directory_path, Directory):    # directory object
        directory_path = directory_path.AbsPath

    state = {}

    def directory_is_modified(process, **kw):
        #pylint: disable=unused-argument
        if not os.path.isabs(directory_path):
            directory_path = os.path.normpath(
                os.path.join(
                    process.RunDirectory,
                    directory_path
                )
            )

        if os.path.isdir(directory_path):
            current_mtime = os.path.getmtime(directory_path)
        else:
            host.WriteDebug(["DirectoryModified", "when"],
                            "directory '{0}' does not exist yet".format(directory_path))
            state["modify_time"] = 0
            return False

        if "modify_time" in state:
            host.WriteDebug(["DirectoryModified", "when"],
                            "directory was last modified at {0}".format(state["modify_time"]))
            return state["modify_time"] < current_mtime

        state["modify_time"] = current_mtime
        return False

    return directory_is_modified


AddWhenFunction(DirectoryExists, generator=True)
AddWhenFunction(DirectoryNotExists, generator=True)
AddWhenFunction(DirectoryModified, generator=True)

AddWhenFunction(DirectoryExists, name='DirExists', generator=True)
AddWhenFunction(DirectoryNotExists, name='DirNotExists', generator=True)
AddWhenFunction(DirectoryModified, name='DirModified', generator=True)

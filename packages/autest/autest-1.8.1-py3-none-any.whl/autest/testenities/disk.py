import os
from typing import Optional, Any
import autest.api
import autest.glb as glb
import hosts.output as host
from autest.common.constructor import call_base, smart_init
from autest.core.testentity import TestEntity

from .directory import Directory
from .file import File


@smart_init
class Disk(TestEntity):

    @call_base(TestEntity=("runable", ))
    def __init__(self, runable):
        self.__files = {}
        self.__dirs = {}

    def File(self,
             name,
             exists: Optional[bool] = None,
             size: Optional[int] = None,
             content: Optional[str] = None,
             execute=None,
             id: str = None,
             runtime: bool = True,
             typename: Optional[str] = None):
        '''
        Creates a new File object.

        Args:
            name:
                The path to the file. This is relative to the runtime state.
            exists:
                Can be set to True to test that the file exists or False to test that it does not exist
                Can be set to a tester object for a custom test.
            size:
                Can be set a integer value greater or equal to 0 to test that file matches the exact size.
                Can be set to a tester object for a custom test.
            execute: currently ignored
            id:
                A custom value that can be used to refer to the file as part of the Disk object later in the test file.
            runtime:
                Can be normally ignored.
                By default this is True which mean the relative path is based on the current sandbox/runtime path is the root.
                If False the relative path is based on the current location of the test file.
            typename:
                Control if the file should be of a certain type.
                This allows creation of File objects that might have extended functionality such as reading and
                writing json files via a dictionary interface.
        '''

        if typename is None:
            ext = os.path.splitext(name)
            # auto select file based on ext
            cls = glb.FileExtMap.get(ext, File)
        else:
            # select file based on typename
            cls = glb.FileTypeMap.get(typename, File)

        tmp = cls(self._Runable, name, exists, size, content, execute, runtime)

        if name in self.__files:
            host.WriteWarning("Overriding file object {0}".format(name))
        self.__files[name] = tmp
        if id:
            self.__dict__[id] = tmp
        return tmp

    def Directory(self, name, exists=None, id=None, runtime=True):
        '''
        Creates a new Directory object.

        Args:
            name:
                The path to the file. This is relative to the runtime state.
            exists:
                Can be set to True to test that the file exists or False to test that it does not exist
                Can be set to a tester object for a custom test
            id:
                a custom value that can be used to refer to the file as part of the Disk object later in the test file
            runtime:
                Can be normally ignored.
                By default this is True which mean the relative path is based on the current sandbox/runtime path is the root.
                If False the relative path is based on the current location of the test file
        '''
        tmp = Directory(self._Runable, name, exists, runtime)
        if name in self.__dirs:
            host.WriteWarning("Overriding directory object {0}".format(name))
        self.__dirs[name] = tmp
        if id:
            self.__dict__[id] = tmp
        return tmp

    def __getitem__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]

        if key in self.__dirs:
            return self.__dirs[key]

        return self.__files[key]


autest.api.AddTestEntityMember(Disk)

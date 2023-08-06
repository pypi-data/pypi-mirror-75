from __future__ import absolute_import, division, print_function
import os

from autest.common.constructor import call_base, smart_init
from autest.core.testentity import TestEntity
import autest.testers as testers
from autest.core.testerset import TesterSet


@smart_init
class Directory(TestEntity):
    '''
    Allows us to test for a file. We can test for existence
    '''

    @call_base(TestEntity=("runable", ))
    def __init__(self, runable, name, exists=True, runtime=True):
        self.__name = name
        self.__runtime = runtime

        # setup testables
        # exists
        self._Register(
            "Directory.{0}.Exists".format(self.__name),
            TesterSet(
                testers.DirectoryExists,
                self,
                self._Runable.FinishedEvent,
                converter=bool,
                description_group="{0} {1}".format("directory", self.__name)),
            ["Exists"])

        self.Exists = exists

    def __str__(self):
        return self.Name

    def GetContent(self, eventinfo):
        return self.AbsPath, ""

    @property
    def AbsPath(self):
        '''
        Absolute path of the file based on the default runtime behavior.
        This is normally the runtime path which maps to the sandbox directory.
        '''
        if self.__runtime:
            return self.AbsRunTimePath
        return self.AbsTestPath

    @property
    def AbsRunTimePath(self):
        '''
        Absolute path of the file based on the runtime path which maps to the sandbox directory.
        '''
        return os.path.normpath(
            os.path.join(self._RootRunable.RunDirectory, self.Name))

    @property
    def AbsTestPath(self):
        '''
        Absolute path of the file based on the test path or the location in which the original test file exists.

        '''
        return os.path.normpath(
            os.path.join(self._RootRunable.TestDirectory, self.Name))

    @property
    def Name(self):
        '''
        The name of the file.
        This is general the path to the file relative to the testing or runtime root.
        It can be an absolute path as well given the file was defined that way

        :getter: returns the name
        '''
        return self.__name

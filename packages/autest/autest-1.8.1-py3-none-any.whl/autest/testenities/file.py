from __future__ import absolute_import, division, print_function

import os

import autest.common.is_a as is_a
import autest.testers as testers
import hosts.output as host
from autest.common.constructor import call_base, smart_init
from autest.core.testentity import TestEntity
from autest.core.testerset import TesterSet

'''
    Allows us to test for a file. We can test for size, existence and content
'''

@smart_init
class File(TestEntity):


    @call_base(TestEntity=("runable", ))
    def __init__(self,
                 runable,
                 name,
                 exists=None,
                 size=None,
                 content_tester=None,
                 execute=False,
                 runtime=True):
        self.__name = name
        self.__runtime = runtime
        self._count = 0
        # setup testables
        des_grp = "{0} {1}".format("file", self.__name)
        # exists
        self._Register(
            "File.{0}.Exists".format(self.__name),
            TesterSet(
                testers.FileExists,
                self,
                self._Runable.FinishedEvent,
                converter=bool,
                description_group=des_grp),
            "Exists")
        # size
        self._Register(
            "File.{0}.Size".format(self.__name),
            TesterSet(
                testers.Equal,
                self.GetSize,
                self._Runable.FinishedEvent,
                converter=int,
                description_group=des_grp,
                description="File size is {0.Value} bytes"),
            "Size")
        # content
        self._Register(
            "File.{0}.Content".format(self.__name),
            TesterSet(
                testers.GoldFile,
                self,
                self._Runable.FinishedEvent,
                converter=lambda x: File(self._Runable, x, runtime=False),
                description_group=des_grp
            ), "Content"
        )
        # Executes
        # self._Register(
        #    "File.{0}.Executes".format(self.__name),
        #    TesterSet(
        #            testers.RunFile,
        #            self,
        #            self._TestRun.EndEvent,
        #            converter=lambda x: File(self._TestRun, x, runtime=False),
        #            description_group=des_grp
        #        ),"Execute"
        #    )

        # Bind the tests based on values passed in

        if exists:
            self.Exists = exists
        if size:
            self.Size = size
        if content_tester:
            self.Content = content_tester
        if execute:
            self.Execute = execute

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
    def Name(self) -> str:
        '''
        The name of the file.
        This is general the path to the file relative to the testing or runtime root.
        It can be an absolute path as well given the file was defined that way.

        :getter: Returns name of file

        '''
        return self.__name

    @Name.setter
    def Name(self, val):
        self.__name = val

    def GetSize(self):
        '''
        The size of the file items in bytes.

        returns:
            The size in bytes or None if it does not exist.
        '''
        try:
            statinfo = os.stat(self.AbsPath)
            return statinfo.st_size
        except:
            return None

    def WriteOn(self, content, event=None):
        '''
        Writes out content to a replacing any existing content in the file.

        Args:
            content:
                A string containing the content to write
                A function can be provided that will write the data itself.
                This function takes accepts one argument of the file object
                to use to write to the file.


            event:
                The event that the write should be trigger with.
                By default, this is the Starting event.


        Examples:

            Write new data in a file

            .. code:: python

                f = tr.Disk.File("data.json")
                d.WriteOn("{data=1}")
        '''

        def action(ev):
            path = os.path.split(self.AbsRunTimePath)[0]
            if not os.path.exists(path):
                os.makedirs(path)
            with open(self.AbsRunTimePath, mode="w") as outfile:
                if is_a.String(content):
                    outfile.writelines(content)
                else:
                    content(outfile)
            return (True, "Writing file {0}".format(self.Name), "Success")

        if event is None:
            event = self._Runable.StartingEvent

        self._Runable._RegisterEvent(
            "File.{0}.WriteOn.{1}".format(self.__name, self._count),
            event,
            testers.Lambda(
                action,
                description_group="Writing File {0}".format(self.__name)))

    def WriteAppendOn(self, content, event=None):
        '''
        Append content to a file.
        If the file does not exist, it will create a new file.

        Args:
            content:
                A string containing the content to write
                A function can be provided that will write the data itself.
                This function takes accepts one argument of the file object
                to use to write to the file.

            event:
                The event it should write on.
                By default, this is the Starting event.

        Examples:

            Write new data in a file, causing it to be different on different event

            .. code:: python

                f = tr.Disk.File("foo.c")
                d.WriteAppendOn("//changed file",tr.FinishedEvent)
        '''
        # content is a string or function taking a file handle
        def action(ev):
            path = os.path.split(self.AbsRunTimePath)[0]
            if not os.path.exists(path):
                os.makedirs(path)
            with open(self.AbsRunTimePath, mode="a+") as outfile:
                if is_a.String(content):
                    outfile.writelines(content)
                else:
                    content(outfile)
            return (True, "Appending file {0}".format(self.Name), "Success")

        if event is None:
            event = self._Runable.StartingEvent

        # content is a string or function taking a file handle
        self._count += 1
        self._Runable._RegisterEvent(
            "File.{0}.WriteAppendOn.{1}".format(self.__name, self._count),
            event,
            testers.Lambda(
                action,
                description_group="Appending File {0}".format(self.__name)))

    def WriteCustomOn(self, func, event=None):
        '''
        Takes a function that will write data to a file when a certain event goes off.
        The functions will be passed a string for the filename to write to.
        The function is responsible for opening and closing the file.
        It should return values based on what testers.Lambda accepts to report the issue to the user.

        Args:
            func:
                A function that takes a file name.
                This function that will open and write data.

            event:
                The event it should write on.
                By default, this is the Starting event.
        '''
        # content is a string or function taking a file handle
        def action(ev):
            return func(self.Name)

        if event is None:
            event = self._Runable.StartingEvent

        # content is a string or function taking a file handle
        self._count += 1
        self._Runable._RegisterEvent(
            "File.{0}.WriteCustomOn.{1}".format(self.__name, self._count),
            event,
            testers.Lambda(
                action,
                description_group="Appending File {0}".format(self.__name)))

    def __iadd__(self, value):
        self.Content += value
        return self.Content

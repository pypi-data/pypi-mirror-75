from __future__ import absolute_import, division, print_function

import abc

from future.utils import with_metaclass

import autest.common.event as event
import autest.common.is_a as is_a
import autest.glb as glb
import autest.testers as testers
import hosts.output as host
from autest.common.constructor import call_base, smart_init

from .delayeventmapper import DelayedEventMapper
from .metaclass import _test_enity__metaclass__
from .stringdict import StringDict
from .testerset import TesterSet
from .variables import Variables

from typing import Dict

# This is the base class needed to define some runable event object
# in the frame work


@smart_init
class Runable(with_metaclass(_test_enity__metaclass__, DelayedEventMapper)):
    '''
    Anything that has testable properties is a runnable.
    This defines the basic logic needed to trigger a tester at the correct time as well as define state needed for a test
    '''

    @call_base(DelayedEventMapper=())
    def __init__(self, parent=None):
         # core events
        self.__SetupEvent = event.Event()
        self.__StartingEvent = event.Event()
        self.__StartedEvent = event.Event()
        self.__RunningEvent = event.Event()
        self.__FinishedEvent = event.Event()
        self.__CleanupEvent = event.Event()

        self.__env = StringDict()
        self.__variables = Variables(
            parent=parent.Variables if parent else {})
        self.__parent = parent
        self.__result = None
        self.__reason = None

    # event accessors
    @property
    def SetupEvent(self) -> event.Event:
        '''
        Called to do any setup logic
        '''
        return self.__SetupEvent

    @property
    def StartingEvent(self) -> event.Event:
        '''
        Called before we start the main logic of the runnable.
        '''
        return self.__StartingEvent

    @property
    def StartedEvent(self) -> event.Event:
        '''
        Called after the main logic has started
        '''
        return self.__StartedEvent

    @property
    def RunningEvent(self) -> event.Event:
        '''
        Called every .1 of second while the runnable logic is executing
        '''
        return self.__RunningEvent

    @property
    def FinishedEvent(self) -> event.Event:
        '''
        Called after the logic of the runnable has finished
        '''
        return self.__FinishedEvent

    @property
    def CleanupEvent(self) -> event.Event:
        '''
        Called to do any cleanup actions
        '''
        return self.__CleanupEvent

    @property
    def _Runable(self):
        return self

    @property
    def _ParentRunable(self):
        return self.__parent

    @property
    def _RootRunable(self):
        if self._ParentRunable is None:
            return self
        return self._ParentRunable._RootRunable

    @abc.abstractmethod
    def _Run(self):
        raise NotImplementedError

    def _do_run(self):
        self._Run()

    def ComposeEnv(self) -> Dict[str,str]:
        ret = {}
        if self.__parent:
            ret = self.__parent.ComposeEnv()
        ret.update(self.__env)
        return ret

    @property
    def Env(self) -> StringDict:
        '''
        The shell environment used for running commands.
        Returns a dictionary type object.
        Items are in the dictionary are only the those set at the current scope.
        This mean a variable set of the Test object will not be seen at the TestRun object.
        To get a fully composed set of values including those of parent TestRun
        or Test object call the ComposeEnv() API.
        Values set at a lower scope override values defined in a parent scope.


        Example:

            use a special feature for the test

            .. sourcecode:: python

                Test.Env["USE_MY_FEATURE1"] = "1"
        '''
        return self.__env

    @Env.setter
    def Env(self, val):
        if not is_a.Dict(val):
            raise TypeError("value needs to be a dict type")
        self.__env = StringDict(val)

    def ComposeVariables(self) -> StringDict:
        '''
        Returns a dictionary of all variable with the parents,
        if any replaces with values of the children.
        '''
        ret = Variables()
        if self.__parent:
            ret = self.__parent.ComposeVariables()
        ret.update(self.__variables)
        return ret

    @property
    def Variables(self):
        '''
        Defines a special Variables object that allows for the dynamic setting of new values.
        Allows for setting of state to be shared for defining tests.
        Values are shared and can be overridden on child objects.

        Example:

        Define a new variable for Port value

        .. sourcecode:: python

            Test.Variables.Port = 8080

            tr=Test.AddTestRun()
            tr.Processes.Default="curl localhost:{0}".format(tr.Variables.Port)

        '''
        return self.__variables

    @Variables.setter
    def Variables(self, val):
        if not is_a.Dict(val):
            raise TypeError("value needs to be a dict type")
        self.__variables.update(val)

    @property
    def _Testers(self):
        ret = []
        for x in self._GetCallBacks():
            if not isinstance(x, TesterSet):
                # this is probally a lambda tester used internally in the code
                ret.append(x[1])
            else:
                ret += [t for t in x._testers if isinstance(
                    t, testers.tester.Tester)]
        return ret

    @property
    def _ChildRunables(self):
        '''
            this need to be overridden if the Runable has children
            that Runables. Default object such as Test and TestRun
            do this.
        '''
        return []

    @property
    def _Result(self):
        if self.__result is None:

            # get any children
            children = self._ChildRunables

            # we have no tests to run?
            if len(self._Testers) == 0 and len(children) == 0:
                self.__result = testers.ResultType.Passed
                self.__result = testers.ResultType.Unknown
                return self.__result

            # get results of this runnable
            self.__result = -1
            for i in self._Testers:
                if self.__result < i.Result:
                    self.__result = i.Result

            # get the results of the children
            for child in children:
                if self.__result < child._Result:
                    self.__result = child._Result

        return self.__result

    @_Result.setter
    def _Result(self, val):
        self.__result = val

    @property
    def _Reason(self):
        return self.__reason

    @_Reason.setter
    def _Reason(self, value):
        self.__reason = value

    # for more detailed extention handling
    def _AddMethod(self, func, name=None):
        m = func.__get__(self)
        name = name if name is not None else func.__name__
        setattr(self, name, m)

    def _AddObject(self, obj, name=None):
        name = name if name is not None else obj.__name__
        setattr(self, name, obj)
        obj.Bind(self)

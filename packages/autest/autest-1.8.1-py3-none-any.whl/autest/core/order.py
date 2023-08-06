from __future__ import absolute_import, division, print_function
import time
from collections import namedtuple

from autest.common.constructor import call_base, smart_init
import autest.common.sort as sort
import autest.common.is_a as is_a
import hosts.output as host

# need better name...  to do later


@smart_init
class Order(object):
    @call_base()
    def __init__(self):

        # items holding state
        self.__startbefore = {}  # {process : metadata}
        self.__startafter = {}
        self.__endbefore = {}
        self.__endafter = {}

        # ready logic
        self.__ready = None
        self.__startup_time = None
        # delay logic
        self.__delay_start = None

    def _setupReadyStart(self, obj, *lst, **kw):
        # validate this is an order object
        if not isinstance(obj, Order):
            host.WriteError(
                "Object must be subclass of autest.core.order.Order")
        readyfunc = kw.get("ready", obj._isReady)
        args = kw.copy()
        try:
            del args["ready"]
        except KeyError:
            pass
        value = readyfunc
        if is_a.Number(value):
            def readyfunc(hasRunFor): return hasRunFor(value)
        elif hasattr(readyfunc, "when_wrapper"):
            readyfunc = readyfunc(**args)
        return readyfunc, args

    def _setupReadyEnd(self, obj, *lst, **kw):
        # validate this is an order object
        if not isinstance(obj, Order):
            host.WriteError(
                "Object must be subclass of autest.core.order.Order")
        readyfunc = kw.get("ready", lambda: True)
        args = kw.copy()
        try:
            del args["ready"]
        except KeyError:
            pass
        value = readyfunc
        if is_a.Number(value):
            def readyfunc(hasRunFor): return hasRunFor(value)
        elif hasattr(readyfunc, "when_wrapper"):
            readyfunc = readyfunc(**args)
        return readyfunc, args

    def StartBefore(self, *lst, **kw):
        '''
        States that you want to start the provided Process object before the called object.
        The optional ready argument can be a number or function to tell when
        these objects should be ready before starting the next process.
        This is useful when certain states or time delays are needed before the next process can start.
        This function has to be added via named arguments.
        Likewise, arguments can be provided to the ready function via named arguments to help control behavior.

        Args:
            lst:
                These are the Process object{s) to start before this Process object.
            ready:
                Named argument that can be provided to tell when the next process should start.
                The value can be a number, which will tell in second how long to wait.
                If the value is a function, the function needs to return True when the state is ready,
                and False when it is not.
                This function should do a quick test and not block the system from running.

            args:
                Extra named arguments that will be pass to the ready function.

        **Example**

            Simple start A before B with no delay

            .. sourcecode:: python

                A=tr.Processes.Process('a', ...)
                B=tr.Processes.Process('b',...)
                B.StartBefore(A)

            Simple start A before B with 1.5 second delay by setting ready logic

            .. sourcecode:: python

                A=tr.Processes.Process('a', ...)
                A.ready=1.5
                B=tr.Processes.Process('b',..)
                B.StartBefore(A)

            Simple start A before B with 1.5 second delay via setting it on the StartBefore

            .. sourcecode:: python

                A=tr.Processes.Process('a', ...)
                B=tr.Processes.Process('b',...)
                B.StartBefore(A,ready=1.5)

            Simple start A and A1 before B with custom function via setting it on the StartBefore

            .. sourcecode:: python

                def custom_delay(file,size):
                    # ...

                A=tr.Processes.Process('a', ...)
                A1=tr.Processes.Process('a1', ...)

                B=tr.Processes.Process('b',...)
                B.StartBefore(A,A1,ready=custom_delay,file="startup.log",size=1024)

        '''
        if lst == () and kw == {}:
            return self.__startbefore
        if lst == () and kw != {}:
            raise SyntaxError

        for obj in lst:
            readyfunc, args = self._setupReadyStart(obj, *lst, **kw)
            host.WriteDebugf(
                ["startbefore"],
                "Setting ready logic to wait for object {0} with readyfunc {1}",
                obj, readyfunc)
            self.__startbefore[obj] = (readyfunc, args)

    def StartAfter(self, *lst, **kw):
        '''
        The same as StartBefore(), but in this case will start the provided
        processes after starting this process.
        See StartBefore() for details on arguments and examples.

        Args:
            lst:
                These are the Process object{s) to start before this Process object.
            ready:
                Named argument that can be provided to tell when the next process should start.
                The value can be a number, which will tell in second how long to wait.
                If the value is a function, the function needs to return True when the state is ready,
                and False when it is not.
                This function should do a quick test and not block the system from running.

            args:
                Extra named arguments that will be pass to the ready function.

        '''
        if lst == () and kw == {}:
            return self.__startafter
        if lst == () and kw != {}:
            raise SyntaxError
        for obj in lst:
            readyfunc, args = self._setupReadyStart(obj, *lst, **kw)
            host.WriteDebugf(
                ["startafter"],
                "Setting ready logic to wait for object {0} with readyfunc {1}",
                obj, readyfunc)
            self.__startafter[obj] = (readyfunc, args)

    def EndBefore(self, *lst, **kw):
        '''
        Helps control the order in which Processes should be shut down when the system
        has to stop the running processes.
        Useful when processes might have nanny processes that might restart other processes,
        or when certain state outputs are dependent on how processes are killed.

        Args:
            lst:
                These are the Process object{s) to start before this Process object.
        '''
        if lst == () and kw == {}:
            return self.__endbefore
        if lst == () and kw != {}:
            raise SyntaxError
        for obj in lst:
            readyfunc, args = self._setupReady(obj, *lst, **kw)
            host.WriteDebugf(
                ["endbefore"],
                "Setting ready logic to wait for object {0} with readyfunc {1}",
                obj, readyfunc)
            self.__endbefore[obj] = (readyfunc, args)

    def EndAfter(self, *lst, **kw):
        '''
        Helps control the order in which Processes should be shut down when the system
        has to stop the running processes.
        Useful when processes might have nanny processes that might restart other processes,
        or when certain state outputs are dependent on how processes are killed.

        Args:
            lst:
                These are the Process object{s) to start before this Process object.
        '''
        if lst == () and kw == {}:
            return self.__endafter
        if lst == () and kw != {}:
            raise SyntaxError
        for obj in lst:
            readyfunc, args = self._setupReady(obj, *lst, **kw)
            host.WriteDebugf(
                ["endafter"],
                "Setting ready logic to wait for object {0} with readyfunc {1}",
                obj, readyfunc)
            self.__endafter[obj] = (readyfunc, args)

    @property
    def DelayStart(self) -> float:
        '''
        Defines a number of seconds to delay the start of the object after it has become ready to start.
        This allows a different way to delay starting a Process or TestRun.
        Useful as a way to effectively "sleep" for a time period before the process or a TestRun starts

        Example:

            Sets a delay in the of 2.5 second for a process to reload data

            .. sourcecode:: python

                Test.Processes.Process("server",cmd="…")
                Tr1=Test.AddTestRun()

                # set some value for the server, Server takes at least two second to
                # reload data
                Tr1.Processes.Default="server_cfg -set value=2"
                Tr1.StartBefore(Test.Processes.server)

                # test that the value was loaded
                Tr2=Test.AddTestRun()

                # delay little over two second to give server time to load data
                Tr1.Processes.Default.DelayStart=2.5
                Tr1.Processes.Default="server_cfg -get value"
                Tr1.Processes.Default.Streams..stdout.Content=testers.ContainsExpression("2","test that value = 2")

            Sets a delay in the of 2.5 second for a TestRun to allow steps from the
            previous TestRun time to go through the system

            .. sourcecode:: python

                tr = Test.AddTestRun()
                tr.DelayStart=5 # delay 5 seconds before start the test run
                tr.Processes.Default.Command = 'python diff.py'
                tr.Processes.Default.ReturnCode=0

        '''
        return self.__delay_start

    @DelayStart.setter
    def DelayStart(self, time: float):
        self.__delay_start = time

    @property
    def Ready(self):
        '''
        Option number or function that defines when the Process is considered to be ready.
        To be ready means that we can start another process that should start after this process.
        If the value is a number, it will be used as a number of seconds to wait before starting the process.
        Otherwise this is normally a function defined in the When space.

        This is exist on TestRun and Test objects however at the moment is does not have any affect.

        '''
        return self.__ready

    @Ready.setter
    def Ready(self, test):
        if is_a.Number(test):
            host.WriteDebugf(
                ["order"],
                "Setting ready logic to wait for {0} second for item {1}",
                test, self._ID)
            self.__ready = lambda hasRunFor: hasRunFor(test)
        elif hasattr(test, "when_wrapper"):
            host.WriteDebugf(["order"],
                             "Setting ready logic to {0} second for item {1}",
                             test, self._ID)
            self.__ready = test()
        else:
            host.WriteDebugf(["order"],
                             "Setting ready logic to {0} second for item {1}",
                             test, self._ID)
            self.__ready = test

    def _isReady(self, *lst, **kw):
        if self.__ready is None:
            host.WriteDebugf(
                ["order", 'when', 'process'],
                "Calling Default isReady() function", )
            return True
        try:
            return self.__ready(*lst, **kw)
        except TypeError:
            return self.__ready()

    # internal functions to testing is ready logic
    def _stopReadyTimer(self):
        self.__startup_time = None

    def _startReadyTimer(self):
        self.__startup_time = time.time()

    def _readyTime(self, curr_time):
        if self.__startup_time is None:
            return 0.0
        else:
            return curr_time - self.__startup_time


# some util functions
ordered_item_t = namedtuple("ordered_item_t", "object readyfunc args")


def SortStartOrderedList(lst, startidx=0):
    '''
        make a flatten list of ordered items, ignores Ready logic
        lst -- list of items to sort based on any extra startXXX() relationships
        startidx -- this is the starting default point everything flows around
    '''
    # make depends mapping
    d = {}
    for i in lst:
        try:
            d[i.Name].extend(i.StartBefore().keys())
        except KeyError:
            d[i.Name] = list(i.StartBefore().keys())
        for k in i.StartAfter().keys():
            if k not in d[i]:
                try:
                    d[k].append(i)
                except KeyError:
                    d[k] = [i]
            else:
                "{0} is already a depends on {1}".format(i.Name, k)

    # Sort the items in the list based on depends mapping
    return sort.depends_back_sort(lst, d)


def SortEndOrderedList(lst, startidx=0):
    '''
        make a flatten list of ordered items, ignores Ready logic
        lst -- list of items to sort based on any extra startXXX() relationships
        startidx -- this is the starting default point everything flows around
    '''
    # make depends mapping
    d = {}
    for i in lst:
        try:
            d[i.Name].extend(i.StartBefore().keys())
        except KeyError:
            d[i.Name] = list(i.StartBefore().keys())
        for k in i.StartAfter().keys():
            if k not in d[i]:
                try:
                    d[k].append(i)
                except KeyError:
                    d[k] = [i]
            else:
                "{0} is already a depends on {1}".format(i.Name, k)

    # Sort the items in the list based on depends mapping
    return sort.depends_back_sort(lst, d)


# these funtions generate a list with visted information in it
# The list that are returned are Fat in that they can contain an item
# more than once. This is because the "ready" requirements for a given process
# can happen for different reason for the same process. For example
# you might want to start a server before one client when port 8080 is ready
# while a different client when port 9090 is read on the same server
# example:
# client.StartBefore(server,ready=When.PortOpen(8080))
# client2.StartBefore(server,ready=When.PortOpen(9090))
# at the moment this only works with processes
# everything else at the moment is a straight depends setup
# ie use of ready does not seem to have value for ordering Tests or TestRuns
# as those items are sequential in nature while Processes are asynchronous,
# and need a delay to help allow the sequential execution to work correctly.


def GenerateStartOrderedList(item):
    '''
        make a flatten list of ordered items
        item -- this is the starting default point everything flows around
    '''

    def append_not_exist(olst, nlst):
        for l in nlst:
            if l not in olst:
                olst.append(l)

    def getlst(data, stack, default_proc):
        ret = []
        for obj, func_info in data.items():
            info = ordered_item_t(obj, func_info[0], func_info[1])
            # break any loops
            if info in stack:
                host.WriteVerbosef(
                    "Ignoring adding {0} to start order as it is already exist, breaking loop.",
                    info.object.Name)
                ret.append(info)
                continue
            stack.append(info)
            ret.extend(getlst(obj.StartBefore(), stack, default_proc))
            ret.append(info)
            ret.extend(getlst(obj.StartAfter(), stack, default_proc))
        return ret

    fat_lst = []

    if item.Command is not None:
        fat_lst.extend(getlst(item.StartBefore(), [], item))
        fat_lst.append(ordered_item_t(item, item._isReady, {}))
        fat_lst.extend(getlst(item.StartAfter(), [], item))
    # flatten the list by taking the last item
    ret = []
    fat_lst.reverse()
    for i in fat_lst:
        if i not in ret:
            ret = [i]+ret
    return ret


def GenerateEndOrderedList(item):
    '''
        make a flatten list of ordered items
        item -- this is the starting default point everything flows around
    '''

    def append_not_exist(olst, nlst):
        for l in nlst:
            if l not in olst:
                olst.append(l)

    def getlst(data, stack, default_proc):
        ret = []

        for obj, func_info in data.items():
            info = ordered_item_t(obj, None, {})
            # break any loops
            if info in stack:
                host.WriteVerbosef(
                    "Ignoring adding {0} to start order as it is already exist, breaking loop.",
                    info)
                continue
            stack.append(info)
            ret.extend(getlst(obj.EndBefore(), stack, default_proc))
            ret.append(info)
            ret.extend(getlst(obj.EndAfter(), stack, default_proc))
        return ret

    fat_lst = []

    if item.Command is not None:
        fat_lst.extend(getlst(item.EndBefore(), [], item))
        fat_lst.append(ordered_item_t(item, None, {}))
        fat_lst.extend(getlst(item.EndAfter(), [], item))

    # flatten the list by taking the last item
    ret = []
    fat_lst.reverse()
    for i in fat_lst:
        if i not in ret:
            ret = [i]+ret

    return ret

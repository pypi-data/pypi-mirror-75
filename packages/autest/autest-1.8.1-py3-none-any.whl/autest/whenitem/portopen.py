''''''
import socket
from typing import Optional, List

import psutil

import hosts.output as host
from autest.api import AddWhenFunction


def PortsOpen(ports: List[int]):
    '''
    Test that all Ports are open via doing doing multipul calls to :func:`PortOpen`
    It will return true when all port return that they are open.

    Args:
        ports: List of port values to check

    '''
    port_lst = []

    for port in ports:
        port_lst.append(PortOpen(port))

    return all(port_lst)


def PortsReady(ports: List[int]):
    '''
    Test that all Ports are open via doing doing multipul calls to :func:`PortReady`.
    It will return true when all port return that they are ready.

    Args:
        ports: List of port values to check

    '''
    port_lst = []

    for port in ports:
        port_lst.append(PortReady(port))

    return all(port_lst)


def PortOpen(port: int, address: Optional[str] = None, timeout: Optional[int] = None, address_family: str = "inet4"):
    '''

    Checks to see if a port is open. This function is more like a stat test in that no traffic happens.
    Only a check that the system sees the port is open. Even if the port is open the server may not be
    ready to accept data. If the code to do a netstat test on the system does not exist the code will
    fallback to a PortReady call


    Args:
        port:
            The port to check.
        address:
            The address to bind to.
        timeout:
            How long to wait before timing out. Ignored unless code falls back to PortReady call.
        address_family:
            The family of space to use. Checks the IPv4 space by default.

    Examples:

        Don't start the curl command until the port on the server is ready

        .. code:: python3

            Test.SkipUnless(Condition.HasProgram("curl","Curl need to be installed on system for this test to work"))

            p=Test.Processes.Process("ts","my-server –port 8080")
            t = Test.AddTestRun("server started properly")
            t.StillRunningAfter = Test.Processes.ts

            p = t.Processes.Default
            p.Command = "curl http://127.0.0.1:8080"
            p.ReturnCode = 0
            p.StartBefore(Test.Processes.ts, ready = When.PortOpen(8080))


    '''

    # If for some reason psutil fails here, we will fall back on the PortReady logic
    ret = False
    try:
        netstate = psutil.net_connections(address_family)
    except:
        netstate = None

    # if no port are being read.. we probally have some system issue with the library
    # and should fall back to older logic
    if netstate:
        # Address/port only ready to use if it is in LISTEN or NONE state
        connections = [i.laddr for i in netstate if i.status == 'LISTEN' or i.status == 'NONE']
        ports = [i.port for i in connections if i.ip == address or address is None]
        if port in ports:
            ret = True
        else:
            ret = PortReady(port, address=address, timeout=timeout)
    else:
        ret = PortReady(port, address=address, timeout=timeout)

    return ret


def PortOpenv4(port: int, address: Optional[str] = None, timeout: Optional[int] = None):
    '''
    The same as :func:`PortOpen`: except it will only check on ipv4 space

    Args:
        port:
            The port to check.
        address:
            The address to bind to.
        timeout:
            How long to wait before timing out. Ignored unless code falls back to PortReady call.

    '''
    return PortOpen(port=port, address=address, timeout=timeout, address_family='inet4')


def PortOpenv6(port: int, address: Optional[str] = None, timeout: Optional[int] = None):
    '''
    The same as :func:`PortOpen`: except it will only check on ipv6 space

    Args:
        port:
            The port to check.
        address:
            The address to bind to.
        timeout:
            How long to wait before timing out. Ignored unless code falls back to PortReady call.

    '''
    return PortOpen(port=port, address=address, timeout=timeout, address_family='inet6')


def PortReady(port: int, address: Optional[str] = None, timeout: Optional[float] = None):
    '''
    Detect that the port is open via trying to connect the address and port.
    This causes some traffic on the host of the port, however this also means that the
    host is more likely to be ready to get traffic.

    Note:
        This does not mean the host is "ready". In such cases a different test of state maybe
        needed, such as sending a test packet/message of some kind that the application understand
        and can send a response to

    Args:
        port:
            The port to check.
        address:
            The address to bind to.
        timeout:
            How long to wait before timing out. Ignored unless code falls back to PortReady call.

    '''

    ret = False

    if address is None:
        address = "localhost"
    if timeout is None:
        timeout = .5
    iaddress = (address, port)
    soc: Optional[socket.socket]
    try:
        soc = socket.create_connection(iaddress, timeout=timeout)
        soc.close()
        ret = True
    except socket.error:
        soc = None
        ret = False
    except socket.timeout:
        soc = None
    host.WriteDebug(["portReady", "when"],
                    "checking port {0} = {1}".format(port, ret))

    return ret


AddWhenFunction(PortsOpen)
AddWhenFunction(PortsReady)
AddWhenFunction(PortOpen)
AddWhenFunction(PortOpenv4)
AddWhenFunction(PortOpenv6)
AddWhenFunction(PortReady)

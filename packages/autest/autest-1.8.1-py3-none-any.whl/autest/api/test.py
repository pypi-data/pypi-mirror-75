from __future__ import absolute_import, division, print_function
import hosts.output as host
import autest.glb as glb
from autest.core.test import Test


def ExtendTest(func, name=None):
    if not glb.running_main:
        return
    if name is None:
        name = func.__name__
    method = func
    setattr(Test, name, method)
    host.WriteVerbose("api",
                      'Added Test extension function "{0}"'.format(name))

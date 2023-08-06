from __future__ import absolute_import, division, print_function
from autest.common.constructor import call_base, smart_init


@smart_init
class Item(object):

    __slots__ = [
        '__ID',
        '__description',
    ]

    @call_base()
    def __init__(self, description, id):

        self.__ID = id
        self.__description = description

    # id should be read only I think
    @property
    def _ID(self):
        return self.__ID

    @property
    def Name(self) -> str:
        '''
        The name used to refer to this object
        '''
        return self.__ID


    @property
    def _Description(self):
        return self.__description

    @_Description.setter
    def _Description(self, val):
        self.__description = val

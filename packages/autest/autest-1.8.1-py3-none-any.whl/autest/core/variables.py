#from __future__ import absolute_import, division, print_function
#from autest.common.constructor import call_base, smart_init
#import autest.common.is_a as is_a

# object inherits dict type


class Variables(dict):
    __slots__ = ('__parent__',)

    def __init__(self, values={}, parent={}):
        super().__init__(values)
        # add check to validate type
        # if not is_a.Dict(parent):
        #raise TypeError("parent most be a dictionary type")
        self.__parent__ = parent

    def __contains__(self, k):
        return super().__contains__(k) or k in self.__parent__

    def __getitem__(self, name):
        if super().__contains__(name):
            return super().__getitem__(name)
        else:
            # it does not so we check the parent is we have one
            return self.__parent__[name]

    def __getattr__(self, name):
        # is this a sloted value?
        if name in Variables.__slots__:
            # return the slotted value
            return super().__getattr__(name)

        # test to see if the value is in our dict
        try:
            return self[name]
        except KeyError:
            # it does not so we check the parent is we have one
            p = self.__parent__
            if p:
                try:
                    return p[name]
                except KeyError:
                    pass
            # if we get here we have an AttributeError
            raise AttributeError("%r has no attribute %r" %
                                 (self.__class__, name))

    def __setattr__(self, name, value):

        if name in Variables.__slots__:
            super().__setattr__(name, value)
            return
        self[name] = value

    def items(self):
        tmp = {}
        tmp.update(self.__parent__)
        tmp.update(self)
        return tmp.items()

    def keys(self):
        tmp = {}
        tmp.update(self.__parent__)
        tmp.update(self)
        return tmp.keys()

    def values(self):
        tmp = {}
        tmp.update(self.__parent__)
        tmp.update(self)
        return tmp.values()

    def __len__(self):
        return len(super().keys() | self.__parent__.keys())

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __repr__(self):
        tmp = {}
        tmp.update(self.__parent__)
        tmp.update(self)
        return tmp.__repr__()

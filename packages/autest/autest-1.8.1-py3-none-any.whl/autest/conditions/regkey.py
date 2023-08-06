
import autest.api as api
from typing import List
import autest.common.reg as reg

# clean this up some mre ( key vs list of keys.. better example to clarify root and key forms)

def HasRegKey(self, root:str, keys:List[str], msg:str):
    '''
    Returns a condition that will test if a given key are found in the registry on windows.

    Args:
        root: The root path to check for the keys under
        keys: the list of one or more keys to check for
        msg: The message to print about the condition.
    '''
    return self.Condition(lambda: reg.has_regkey(root, keys), msg, True)

# def RegistryKeyEqual(self,key,value):
# pass

api.ExtendCondition(HasRegKey)

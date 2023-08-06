"""

SOURCE:
    `Flattening a list of dicts of lists of dicts (etc) of unknown depth in Python 
    (nightmarish JSON structure)`

    http://stackoverflow.com/questions/8477550/flattening-a-list-of-dicts-of-lists-of-dicts-etc-of-unknown-depth-in-python-n

DESCRIPTION:
    Used for library parsing testing
    Should not be modified unless modifying the tests listed below


ARGS:
    NestedObject
        Type:
            Any possible combination of nested objects, lists, structures, classes, strings, numbers
            OR
            A single non-iterable object -> (which is read as `[NestedObject]` )
        Description:
            See Type

    PrintExtra


RETURNS:
    NestedObjectFlat
        Type:
            Python List
        Description:
            Contains ordered non-iterable elements of the `NestedObject` provided as arg

TESTS:
    NONE! .... great....
    

"""
import numpy
import pprint

from .Type_Iterable import Type_Iterable

def Library_NestedObjectFlatten(
    NestedObject = None,
    PrintExtra = False,
    ):
    
    #If the nested object happens to not really be a nested object, 
    #   we turn it into a list of 1 element:
    if (not Type_Iterable(NestedObject)):
        NestedObject = [NestedObject]
        return NestedObject

    #Swiped and modified from stack overflow:
    def flatten(l):
        out = []

        #TODO: Replace the first three statements with `if Type_Iterable.Main()` then cast to list and extend
        if isinstance(l, (set)):
            l = list(l)
        if isinstance(l, (list, tuple)):
            for item in l:
                out.extend(flatten(item))
        elif isinstance(l, (dict)):
            for dictkey in list(l.keys()):
                out.extend(flatten(l[dictkey]))
        elif isinstance(l, (str, int, float)):
            out.append(l)
        elif isinstance(l , (numpy.ndarray, numpy.generic) ):
            #print 'IS NUMPY ARRAY'
            #for item in list( l.flatten() ):
            #    out.extend( flatten( item ) )
        
            out.extend( list( l.flatten() ))

        else: #Unkown type -> then we append the flat list with the item
            out.append(l)
            
        return out

    NestedObjectFlat = flatten(NestedObject)

    return NestedObjectFlat













"""
if (type(NestedObject) == type({})):
    NestedObjectFlat = [value for (key, value) in sorted(NestedObject.items())]

else:
    NestedObjectFlat = list(NestedObject)
"""


















































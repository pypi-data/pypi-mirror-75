
"""
SOURCE:




DESCRIPTION:

    This implements what is known as a 
        `Duck typing`

    Does it quack?
    Does it look like a duck?

        
ARGS:
    NumberCandidate
        Description:
            The object of which to check if it is an number python object

RETURNS:
    True on number
    False on NOT number


"""
import numpy
def Type_Number(
    NumberCandidate = None
    ):

    Result = None

    if isinstance(NumberCandidate, (float, int, complex)):
        return True

    try:
        if numpy.isinf(NumberCandidate):
            return True
    except:
        pass

    try:
        NumberFloat = float(NumberCandidate)
        NumberInt = int(NumberCandidate)
        NumberCandidate + 1
        NumberCandidate + 1.

    except TypeError:
        # not number
        Result = False
    except ValueError:
        # not number
        Result = False

    else:
        # number
        Result = True

    return Result



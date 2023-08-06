"""
SOURCE:
    Mind of Douglas Adams
DESCRIPTION:
    Checks if each element of one iterable, is an element in another iterable
    Returns true or false
ARGS:
    CheckArguments
        Type:
            python boolean
        Description:
            if true, checks the arguments with conditions written in the function
            if false, ignores those conditions
    PrintExtra
        Type:
            python integer
        Description:
            if greater than 0, prints addional information about the function
            if 0, function is expected to print nothing to console
            Additional Notes:
                The greater the number, the more output the function will print
                Most functions only use 0 or 1, but some can print more depending on the number
    IterableSubsetCandidate
        Type:
            <type 'NoneType'>
        Description:
    IterableParentCandidate
        Type:
            <type 'NoneType'>
        Description:
RETURNS:
    Result
        Type:
        Description:
"""
from .Library_NestedObjectFlatten import Library_NestedObjectFlatten

def Library_IterableSubset(
    IterableSubsetCandidate= None,
    IterableParentCandidate= None,
    CheckArguments = True,
    PrintExtra = False,
    ):

    Result = None

    if (CheckArguments):
        ArgumentErrorMessage = ""

        if (len(ArgumentErrorMessage) > 0 ):
            if(PrintExtra):
                print("ArgumentErrorMessage:\n", ArgumentErrorMessage)
            raise Exception(ArgumentErrorMessage)


    IterableSubsetCandidate = set(Library_NestedObjectFlatten(IterableSubsetCandidate))
    IterableParentCandidate = set(Library_NestedObjectFlatten(IterableParentCandidate))


    IterableIntersection = set.intersection(*[IterableSubsetCandidate, IterableParentCandidate])


    if (IterableIntersection == IterableSubsetCandidate):
        Result = True
    else:
        Result = False

    return Result 





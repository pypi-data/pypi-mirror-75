"""
SOURCE:
    Mind of Douglas Adams
DESCRIPTION:
    Is it a sympy expression?
    yes/no

    Because integers and floats native to python can interact with sympy functions
    through mathematical operations, int, float, and number types are allowed

ARGS:
    PrintExtra
        Type:
            python integer
        Description:
            if greater than 0, prints addional information about the function
            if 0, function is expected to print nothing to console
            Additional Notes:
                The greater the number, the more output the function will print
                Most functions only use 0 or 1, but some can print more depending on the number
    SympyExpressionCandidate
        Type:
            any
        Description:
            candidate for a sympy expression
RETURNS:
    Result
        Type:
        Description:
"""
import sympy
import sympy.core

from .Type_Number import Type_Number

def Type_SympyExpression(
    SympyExpressionCandidate = None,
    PrintExtra = False,
    ):

    Result = False

    if ( \
        isinstance( SympyExpressionCandidate,  tuple(sympy.core.all_classes) ) \
        or Type_Number(SympyExpressionCandidate)
        ):
        Result = True

    elif(PrintExtra):
        print(str(SympyExpressionCandidate) + 'is not a sympy expression...')

    return Result 

























"""
SOURCE:
    Mind of Douglas Adams
DESCRIPTION:
    Gets the coefficients from an abitrary sympy expression
    Returns a dictionary thing which has the terms as keys, and coefficient values as values
    Keys the terms in a logical way so as to be able to compare the results from
    two sympy exrpessions.

    http://stackoverflow.com/questions/22955888/how-to-extract-all-coefficients-in-sympy

    Note -> for practical comparison, floats are evaluated in the expression,
        This way they are pulled OUT of the terms, 
        and 
        the COEFFICIENTS HAVE ALL THE FLOAT VALUES inside them



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
    SympyExpression
        Type:
            <type 'NoneType'>
        Description:
RETURNS:
    Result
        Type:
        Description:
"""

import sympy

from .Library_SympyExpressionSimplify import Library_SympyExpressionSimplify

def Library_SympyExpressionCoefficients(
    SympyExpression= None,
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


    #for Variable in SympyExpression.free_symbols:
    #    SympyExpression = SympyExpression.collect(Variable)

    #SympyExpressionPoly = sympy.Poly(SympyExpression)

    #SympyExpressionPolyTerms = SympyExpressionPoly.all_monoms()
    #SympyExpressionPolyCoeffs = SympyExpressionPoly.all_coeffs()

    #SympyExpressionDict = {}
    #for Term, Coef in zip(SympyExpressionPolyTerms,SympyExpressionPolyCoeffs):
    #    SympyExpressionDict[Term] = Coef

    SympyExpressionDict = Library_SympyExpressionSimplify(SympyExpression).as_coefficients_dict()   




 
    #SympyExpressionDictValues = SympyExpressionDict.values()

    #print 'SympyExpression', SympyExpression
    #print 'SympyExpressionDict', SympyExpressionDict
    #print 'SympyExpressionDictValues', SympyExpressionDictValues

    Result = SympyExpressionDict

    return Result 







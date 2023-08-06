"""
SOURCE:
    http://docs.sympy.org/dev/gotchas.html

DESCRIPTION:
    Checks to see if an iterable of sympy expressions are ALL mathematically equivelent to each other
    WARNING: 
        Current Implementation is not robust. 
        Only Works for basic summations and products 
        No identy substitutions are attempted
        i.e. The following do not work:
            e^(i*x) != cos(x) + i*sin(x) #Euler Identity
            sin(.5*x) = (-1) **(abs(x/2*pi)) * sqrt( (1-cos(x)) / 2. ) #Half angle formula for sin
    TODO:
        http://mathworld.wolfram.com/Half-AngleFormulas.html
ARGS:
    CheckArguments
        Type:
            python boolean
        Description:
            if PrintExtra, checks the arguments with conditions written in the function
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
    SympyExpressions
        Type:
            Type_Iterable
                <type 'sympy.core.expression'>
        Description:
RETURNS:
    Result
        Type:
        Description:
"""
import sympy
import numpy
import inspect
#------------------------------------------------------------------------------
from .Type_SympyExpression import Type_SympyExpression
from .Type_Iterable import Type_Iterable
from .Library_SympyExpressionSimplify import Library_SympyExpressionSimplify
from .Library_StringExpressionToSympyExpression import Library_StringExpressionToSympyExpression
from .Library_SympyExpressionCoefficients import Library_SympyExpressionCoefficients
from .Library_SympyExpressionPrintInfo import Library_SympyExpressionPrintInfo
from .Library_SympyExpressionRestrictVariables import Library_SympyExpressionRestrictVariables
#------------------------------------------------------------------------------

def Library_SympyExpressionEquality(
    SympyExpressions = None,
    HardDifferenceMax = None,
    OrderOfMagnitudeRatioMax = None,
    CheckArguments = True,
    PrintExtra = False,
    ):

    Result = True

    if (CheckArguments):
        ArgumentErrorMessage = ""

        if (not Type_Iterable(SympyExpressions) ):
            ArgumentErrorMessage += '`SympyExpressions` must be of `Type_Iterable` \n'

        for Expression, ExpressionIndex in zip(SympyExpressions, list(range(len(SympyExpressions))) ):
            if (not Type_SympyExpression(Expression)):
                ArgumentErrorMessage += 'Expression in SympyExpressions is not `Type_SympyExpression`:\n'
                ArgumentErrorMessage += '  SympyExpressions[' + str(ExpressionIndex) +']: '+str(Expression) + ' \n'

        if (len(ArgumentErrorMessage) > 0 ):
            if(PrintExtra):
                print("ArgumentErrorMessage:\n", ArgumentErrorMessage)
            raise Exception(ArgumentErrorMessage)

    PrintExtra = False
    if (HardDifferenceMax is None):
        HardDifferenceMax = 0.0


    Expression0 = SympyExpressions[0]
    if (PrintExtra):
        print('Expression0', Expression0)
        Library_SympyExpressionPrintInfo(Expression0)

    SimplifiedExpression0 = Library_SympyExpressionSimplify(Expression0)
    if (PrintExtra):
        print('SimplifiedExpression0', SimplifiedExpression0)
        Library_SympyExpressionPrintInfo(SimplifiedExpression0)

    for ExpressionK in SympyExpressions:
        if (PrintExtra):
            print('\nExpressionK', ExpressionK)
            Library_SympyExpressionPrintInfo(ExpressionK)

        SimplifiedExpressionK = Library_SympyExpressionSimplify(ExpressionK)
        if (PrintExtra):
            print('SimplifiedExpressionK', SimplifiedExpressionK)
            Library_SympyExpressionPrintInfo(SimplifiedExpressionK)


        for Symbol0, SymbolK in zip(Expression0.free_symbols, ExpressionK.free_symbols):
            if (PrintExtra):
                print('   Symbol0', Symbol0)
                print('   SymbolK', SymbolK)
                print('   Symbol0.is_real', Symbol0.is_real)
                print('   SymbolK.is_real', SymbolK.is_real)

            if (Symbol0.is_real != SymbolK.is_real):
                Result = False
                if (PrintExtra): print('   Symbol0.is_real != Symbol.is_real')
                break


        #ExpressionDifference = SimplifiedExpression - SimplifiedExpression0
        SimplifiedExpressionCoefficients0 = Library_SympyExpressionCoefficients(SimplifiedExpression0 + 1.)
        SimplifiedExpressionCoefficientsK = Library_SympyExpressionCoefficients(SimplifiedExpressionK + 1.)

        for Term0, TermK in zip(SimplifiedExpressionCoefficients0, SimplifiedExpressionCoefficientsK ):
            #Pull the Coefficients out
            Coefficient0 = SimplifiedExpressionCoefficients0[ Term0 ]
            CoefficientK = SimplifiedExpressionCoefficientsK[ TermK ]

            if (PrintExtra):
                print('Term0', Term0)
                print('TermK', TermK)
                print('Coefficient0', Coefficient0)
                print('CoefficientK', CoefficientK)

            #Get the term difference:
            TermDifferenceRestricted = Library_SympyExpressionRestrictVariables(
                    SympyExpression = (Term0 - TermK),
                    Restrictions =  {'real':True},
                    )

            TermDifferenceRealPart = sympy.functions.re( TermDifferenceRestricted )
            TermDifferenceImagPart = sympy.functions.im( TermDifferenceRestricted )
            TermDifference = Library_SympyExpressionSimplify( TermDifferenceRealPart + TermDifferenceImagPart).evalf()
            #TermDifference = sympy.functions.re( TermDifference ) + sympy.functions.im( TermDifference )
            if (PrintExtra): print('TermDifference', TermDifference)

            #Get the coefficient difference:
            CoefficientDifference = Library_SympyExpressionSimplify((Coefficient0 - CoefficientK)).evalf()
            if (PrintExtra): print('CoefficientDifference', CoefficientDifference)

            #Compare the terms:
            if (Term0 != TermK) :
                try:
                    if (TermDifference > HardDifferenceMax):
                        Result = False
                        break
                except:
                    if(PrintExtra): print('Term0 != TermK')
                    if(PrintExtra): print(Term0, '!=', TermK)
                    Result = False
                    break

            #Compare the coefficients:
            if (Coefficient0 != CoefficientK) :
                try:
                    if ( CoefficientDifference > HardDifferenceMax ):
                        if (PrintExtra): print('CoefficientDifference > HardDifferenceMax', end=' ') 
                        if (PrintExtra): print(CoefficientDifference,  '>',  HardDifferenceMax)
                        Result = False
                        break
                except:
                    if(PrintExtra): print('Coefficient0 != CoefficientK')
                    if(PrintExtra): print(Coefficient0, '!=', CoefficientK)
                    Result = False
                    break




    return Result 




















"""
SOURCE:
    Mind of Douglas Adams
DESCRIPTION:
    Prints handy information about a sympy expression
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
def Library_SympyExpressionPrintInfo(
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

    print('SympyExpression', SympyExpression)

    print(len(SympyExpression.free_symbols), 'Symbols:')
    for Symbol in SympyExpression.free_symbols:
        print('   Symbol', Symbol)
        print('   Symbol.is_real', Symbol.is_real)




    return Result 












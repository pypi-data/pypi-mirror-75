"""
SOURCE:
    Mind of Douglas Adams
DESCRIPTION:
    Places a list of rescrictions on a list variables
    If None is provided as the restrictions, then all restrictions are removed
    If None is provided for the variables, the ALL variables are effected by the restriction setting
    WARNING NOTE: (Soft Warning -> Not system dangerous) 
        The default arguments of None for this function, 
        Have a tendency to make serious changes to the expression passed in
        This may be counter intuitive, but the choice was made to avoid 
            passing strings for special cases, 
            extra variables for special cases
        It is safe in a way, that the args are not passed by reference
        new copies are made, and returned to the invoker as usual
    WARNING SUMMARY: (Soft Warning -> Not system dangerous) 
        If you don't want this function to do anything... Don't invoke it!!
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
    Restrictions
        Type:
            <type 'dict'>
        Description:
            restriction input name : property

    VariableNames
        Type:
            <type 'list'> of <type 'str'>
        Description:
            List of strings each of which is a free variable in the sympy expression
RETURNS:
    Result
        Type:
        Description:
"""

import sympy

from .Library_IterableSubset import Library_IterableSubset

def Library_SympyExpressionRestrictVariables(
    SympyExpression = None,
    Restrictions    = None,
    VariableNames   = None,
    CheckArguments  = True,
    PrintExtra      = False,
    ):
    #PrintExtra = True

    #Args have `None` put as a variable defaults on purpose:
    #   -> `None` can be passed by name explicitly this way 
    if (Restrictions is None): 
        Restrictions = {} #no restrictions on the variables --> is NOT the same thing as leaving them unchanged.

    if (VariableNames is None):
        VariableNames = [str(var) for var in SympyExpression.free_symbols]

    Result = None

    if (CheckArguments):
        ArgumentErrorMessage = ""

        #Get the VariableNames from the sympy expression:
        AllVariableNames = [str(var) for var in SympyExpression.free_symbols]
        AllVariableNameCount = len(AllVariableNames)
        if (PrintExtra):
            print('AllVariableNameCount', AllVariableNameCount)
            print('AllVariableNames')
            print(AllVariableNames)

        if not Library_IterableSubset(
            IterableSubsetCandidate= VariableNames,
            IterableParentCandidate= AllVariableNames
            ):
            ArgumentErrorMessage += '`VariableNames` provided must match free variable names in the sympy expression\n'

        if (len(ArgumentErrorMessage) > 0 ):
            if(PrintExtra):
                print("ArgumentErrorMessage:\n", ArgumentErrorMessage)
            raise Exception(ArgumentErrorMessage)

    #x = sympy.Symbol('x', real=True)
    NewExpression = SympyExpression
    for VariableName in VariableNames:
        NewVariable = sympy.Symbol(VariableName, **Restrictions)
        if (PrintExtra):
            print('VariableName', VariableName)
            print('Restrictions', Restrictions)
            print('NewVariable.is_real', NewVariable.is_real)
        #Find the original variable in the variable set which needs to be replaced...
        VariableToReplace = None
        for OriginalVariable in SympyExpression.free_symbols:
            if OriginalVariable.name == VariableName:
                VariableToReplace = OriginalVariable

        NewExpression = NewExpression.subs(VariableToReplace, NewVariable)

    Result = NewExpression
    return Result 






















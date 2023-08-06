"""
SOURCE:

    Mind of Douglas Adams   

DESCRIPTION:

    Prints EVERYTHING that it can about an exception object
    
    Trys its best to make it readable


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

RETURNS:
    Result
        Type:
            <type 'obj'>
        Description:
            Wrapped function
"""


import traceback

def Library_PrintExceptionObject(
    ExceptionObject = None,
    CheckArguments = False, #By default, we don't want to raise any new exceptions by invoking this function
    PrintExtra = False,
    ):

    if (CheckArguments):
        ArgumentErrorMessage = ""

        if (ExceptionObject is None):
            ArgumentErrorMessage += '`ExceptionObject` must not be None\n'

        if (len(ArgumentErrorMessage) > 0 ):
            if(PrintExtra):
                print("ArgumentErrorMessage:\n", ArgumentErrorMessage)
            raise Exception(ArgumentErrorMessage)

    print('\n\n')
    print('---------------------------------------')
    print('Printing ExceptionObject Below...')

    try:
        ExceptionObjectString = str(ExceptionObject)
        print('-----ExceptionObjectString:--------')
        print('')
        print(ExceptionObjectString)
        print('')

        TraceBackString = traceback.format_exc()
        print('-----TraceBackString:--------------')
        print('')
        print(TraceBackString)
        print('')

    except:
        # Expectation on invoking this print statement is never to cause problems
        # we want to be EXTREMELY generous on this function call. 
        pass 

    print('...Done Printing ExceptionObject Above')
    print('---------------------------------------')
    print('\n\n')










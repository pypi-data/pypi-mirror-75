"""
SOURCES:
    http://stackoverflow.com/questions/3394835/args-and-kwargs

        >>> def print_three_things(a, b, c):
        ...     print 'a = {0}, b = {1}, c = {2}'.format(a,b,c)
        ...
        >>> mylist = ['aardvark', 'baboon', 'cat']
        >>> print_three_things(*mylist)
        a = aardvark, b = baboon, c = cat

DESCRIPTION:
    Allows for saving time when writing tests, by
        doing the loop, 
        keeping track of the test success,
        checking results against expected results
        Passing in the args contained within the  `ArgSetExpectedResultCombos`
        

ARGS:
    FunctionToTest
        Type: Python (Method / function / routine)
        Description:
        

    ArgSetExpectedResultCombos
        Description:
            Structure containing all the args with which to pass into the `FunctionToTest`

    OrderOfMagnitudeRatioMax
        Type: Python Float
        Description:
            None provided -> ignored 
            Maximum distance between any expected result and the actual result of the function

    HardDifferenceMax:
        Type: Python Float
        Description:
            None provided -> ignored 
            Maximum absolute distance between any expected result and the actual result of the function

    DoEqualityCheck
        Type: Python Bool   
        Description:
            Checks that non-numerical, non-iterable values are exactly equal within the result
        Default: True

    ResultOrderMatters:
        Type: Python Bool
        Description:
            None provided -> ignored 
            Each expected result must be some type of iterable object for this to make sense
            If the expected result is nested, nested order is assumed to matter

    MinFlatResultLength
        Type: Python Int
        Description:
            None provided -> ignored 
            Expected result, when iterable, and flattened if nested, is checked against this value

RETURNS:
    TestSuccesses
        Type: Python List
        Description:
            Each value corresponds to a test success result
            If all the tests succeed expect to return 
                [True, True, .... True]
            If only the 4th test fails, expect to return 
                [True, True, True, False, True, ... True]

"""


import numpy
import pprint
import collections
import traceback
#------------------------------------------------------------------------------
from .Library_TestResultCheck import Library_TestResultCheck
from .Library_PrintFullTestSuccess import Library_PrintFullTestSuccess

def Library_TestLooper(
    FunctionToTest = None,
    ArgSetExpectedResultCombos = None,

    OrderOfMagnitudeRatioMax = None,
    HardDifferenceMax = None,
    DoEqualityCheck = True,
    DoContainmentCheck = False,
    MinFlatResultLength = None,
    MaxFlatResultLength = None,
    ResultOrderMatters = True, 

    EqualityCheckFunction = None,

    StopAfterTestNumber = None,


    CheckArguments = True,
    PrintExtra = True,
    ):

    FullTestSuccess = True

    if( CheckArguments):
        ArgumentErrorMessage = ""

        #If any errors - terminate
        if ( len( ArgumentErrorMessage ) ):
            raise Exception( ArgumentErrorMessage)

    TestSuccesses = []

    k = 0
    for ArgSet, ExpectedResult in ArgSetExpectedResultCombos:

        #To allow the user to prioritize only doing a few tests in the arg combo list -> 
        #   Created stop count -> which allows only the first few tests to be run. 
        #   In final commited codes, this should almost always be passed in as None
        #   however when debugging specific tests,  
        #   it can be annoying to allow all tests to run each time a small modification is made
        #   to the library which is being debugged
        if StopAfterTestNumber is not None:
            if StopAfterTestNumber < k:
                break

        print("-----------------------------------------------------------------")
        print("Running Test ", k)

        SingleResultCorrectnessCheck = True
        try:
            if (PrintExtra):
                print(' ArgSet:')
                items = list(ArgSet.items())
                items.sort()
                pprint.pprint( items, indent=4)
                print('')

            Result = None
            try:
                Result = FunctionToTest(
                    **ArgSet #*ArgSet #**kwargs python wizzardry -> unpacks the ArgSet as named args into the function call
                )
            except Exception as E:
                Result = Exception('')
                print('\nFunction Failed to execute, printing exception below:\n')
                print(str(E))
                traceback.print_exc()
                print('\nCorrectness Checker now will see if the exception is expected...\n')

            #Run our checker on a single ArgSet, against a single Expected Result
            SingleResultCorrectnessCheck = Library_TestResultCheck(
                Result = Result,
                ExpectedResult = ExpectedResult,

                OrderOfMagnitudeRatioMax = OrderOfMagnitudeRatioMax,
                HardDifferenceMax = HardDifferenceMax,
                DoEqualityCheck = DoEqualityCheck,
                DoContainmentCheck = DoContainmentCheck,
                MinFlatResultLength = MinFlatResultLength,
                MaxFlatResultLength = MaxFlatResultLength,
                ResultOrderMatters = ResultOrderMatters, 

                EqualityCheckFunction = EqualityCheckFunction,

                CheckArguments = CheckArguments,
                PrintExtra = PrintExtra,
                )


            if ( SingleResultCorrectnessCheck ):
                print(' Single Test Success')

            else:
                print(' ArgSet:')
                pprint.pprint( ArgSet )
                print(' Result:')
                pprint.pprint( Result  )
                print(' ExpectedResult:')
                pprint.pprint( ExpectedResult )
                print('')
                print('                 !!!                     !!!')
                print('                     Single Test Failure')
                print('                 !!!                     !!!')
                print('')

        except Exception as E:
            print(' Exception In an execution attempt within the test looper loop.')
            print(' Exception is printed below loop will continue afterwards.')
            print(' ')
            print(str(E))
            traceback.print_exc()
            SingleResultCorrectnessCheck = False
            
        TestSuccesses.append( SingleResultCorrectnessCheck )
        FullTestSuccess = FullTestSuccess and SingleResultCorrectnessCheck
        k += 1

    if (PrintExtra):
        print(' TestSuccesses')
        print(' ', TestSuccesses)
    Library_PrintFullTestSuccess(FullTestSuccess)

    return TestSuccesses









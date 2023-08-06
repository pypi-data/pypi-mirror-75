
"""

DESCRIPTION:
    Used for library testing
    Inherits directly from Library_TestLooper
    
ARGS:
    Inherits directly from Library_TestLooper

RETURNS:
    CorrectnessCheck
        Type: Python Bool
    Description:
        Value corresponds to a test success result
        If all elements of the result provided are good under the conditions specfied in args:
            Returns True
        Else:
            Returns False
 

TESTS:
    Test_LibraryDependecyList
    Test_ExampleLibraryGood0

"""
import pprint
import pickle

from .Library_NestedObjectFlatten import Library_NestedObjectFlatten
from .Library_OrderOfMagnitudeRatioSmallCheck import Library_OrderOfMagnitudeRatioSmallCheck
from .Library_EqualityCheck import Library_EqualityCheck
from .Library_HardDifferenceSmallCheck import Library_HardDifferenceSmallCheck
from .Type_Number import Type_Number
from .Type_Iterable import Type_Iterable

#import Library_ComponentExtract
def Library_TestResultCheck(
    Result = None,
    ExpectedResult = None,

    OrderOfMagnitudeRatioMax = None,
    HardDifferenceMax = None,

    DoEqualityCheck = True,
    DoContainmentCheck = False,
    MinFlatResultLength = None,
    MaxFlatResultLength = None,
    ResultOrderMatters = True, 


    EqualityCheckFunction = None,

    CheckArguments = True,
    PrintExtra = False,
    ):

    #If the expected result is an exception:
    if (isinstance(ExpectedResult, (Exception) ) ):
        CorrectnessCheck = True
        if (not isinstance(Result, (Exception) ) ):
            CorrectnessCheck = False


        return CorrectnessCheck

    OrderOfMagnitudeRatioSmallCheckResult = True
    HardDifferenceSmallCheckResult = True
    EqualityCheck = True
    ContainmentCheck = True
    NumberResultsCheck = True

    #Print the result and the expected result:
    print('UnflattenedResult', Result)
    print('UnflattenedExpectedResult', ExpectedResult)

    #Cast the Result and the ExpectedResult to flattened lists:
    Result = Library_NestedObjectFlatten(Result)
    print('FlattenedResult', Result)
    ExpectedResult = Library_NestedObjectFlatten(ExpectedResult)
    print('FlattenedExpectedResult', ExpectedResult)


    NumberResults = len(Result)
    NumberExpectedResults = len(ExpectedResult)
    print('NumberResults', NumberResults)
    print('NumberExpectedResults', NumberExpectedResults)


    #If order doesn't matter, then reorder the results (reorder them with ANY sorting method):
    if ( ResultOrderMatters == False):
        Result = sorted(Result, key=lambda ObjectItem: pickle.dumps(ObjectItem)  ) 
        ExpectedResult = sorted(ExpectedResult, key=lambda ObjectItem: pickle.dumps(ObjectItem))


    print('Sorted Result')
    pprint.pprint( Result )
    print('Sorted ExpectedResult')
    pprint.pprint( ExpectedResult )

    #Check Lengths
    if (MinFlatResultLength is None):
        MinFlatResultLength = NumberExpectedResults
    if (MaxFlatResultLength is None):
        MaxFlatResultLength = NumberExpectedResults
    print('MinFlatResultLength', MinFlatResultLength)
    NumberResultsCheck = ( NumberResults >= MinFlatResultLength ) and ( NumberResults <= MaxFlatResultLength )
    print('NumberResultsCheck', NumberResultsCheck)

    #Loop through and check value correctness now:
    ValuesMatter = (OrderOfMagnitudeRatioMax is not None) or (HardDifferenceMax is not None) or (DoEqualityCheck)
    print('ValuesMatter', ValuesMatter)

    if (ValuesMatter):
        CurrentResultNumber = 0
        while (CurrentResultNumber < NumberExpectedResults):
            CurrentResult = Result[CurrentResultNumber]
            CurrentExpectedResult = ExpectedResult[CurrentResultNumber]



            SingleEqualityCheck = True
            SingleOrderOfMagnitudeRatioSmallCheck = True
            SingleHardDifferenceSmallCheck = True

            #We know the result is a number
            if ( Type_Number( CurrentExpectedResult )  ):
                #Cast the number to same type so each time comparison works
                CurrentExpectedResult = complex(CurrentExpectedResult).real + complex(CurrentExpectedResult).imag
                CurrentResult = complex(CurrentResult).real + complex(CurrentResult).imag
                if ( OrderOfMagnitudeRatioMax is not None ):
                    SingleResultOrderOfMagnitudeRatioSmallCheckResult = Library_OrderOfMagnitudeRatioSmallCheck(
                        CurrentResult , 
                        CurrentExpectedResult, 
                        OrderOfMagnitudeRatioMax
                        )
                    if (not SingleResultOrderOfMagnitudeRatioSmallCheckResult):
                        print(CurrentResult, " !~ ", CurrentExpectedResult)

                    OrderOfMagnitudeRatioSmallCheckResult = OrderOfMagnitudeRatioSmallCheckResult and SingleResultOrderOfMagnitudeRatioSmallCheckResult


                if (HardDifferenceMax is not None) :
                    SingleValueHardDifferenceSmallCheckResult = Library_HardDifferenceSmallCheck(
                        CurrentResult, 
                        CurrentExpectedResult, 
                        HardDifferenceMax
                        ) 
                    if (not SingleValueHardDifferenceSmallCheckResult):
                        print(CurrentResult, " != ", CurrentExpectedResult)
                    HardDifferenceSmallCheckResult = HardDifferenceSmallCheckResult and SingleValueHardDifferenceSmallCheckResult


            #We know the result is a python function:
            elif (   str(type(CurrentExpectedResult)) == "<type 'function'>" ):
                print('Expected result is a function to test...')
                print('TODO..')
                print('Function.__code__')
                print(CurrentExpectedResult.__code__)

            #We know the result is not a number:
            else:
                if (DoEqualityCheck ):
                    if (EqualityCheckFunction is None):
                        EqualityCheckFunction = Library_EqualityCheck
                    #print 'HardDifferenceMax (in Lib Test Res Check)', HardDifferenceMax
                    SingleEqualityCheck = EqualityCheckFunction( 
                        (CurrentResult,  CurrentExpectedResult), 
                        HardDifferenceMax = HardDifferenceMax,
                        OrderOfMagnitudeRatioMax = OrderOfMagnitudeRatioMax, 
                        )
                    EqualityCheck = EqualityCheck and SingleEqualityCheck
                if (DoContainmentCheck):
                    SingleContainmentCheck = CurrentExpectedResult in CurrentResult
                    ContainmentCheck = ContainmentCheck and SingleContainmentCheck

            #Print for comparison visually 
            if (PrintExtra):
                print('   CurrentResult', CurrentResult)
                print('   CurrentExpectedResult', CurrentExpectedResult)
                if (not SingleEqualityCheck):
                    print('      SINGLE EQUALITY CHECK FAILED  (' , str(CurrentResult), ' != ', str(CurrentExpectedResult), ')')

            CurrentResultNumber += 1


    #Aggregate Correctness:
    if (PrintExtra):
        print(' OrderOfMagnitudeRatioSmallCheckResult', OrderOfMagnitudeRatioSmallCheckResult)
        print(' HardDifferenceSmallCheckResult', HardDifferenceSmallCheckResult)
        print(' EqualityCheck', EqualityCheck)
        print(' NumberResultsCheck', NumberResultsCheck)

    CorrectnessCheck = OrderOfMagnitudeRatioSmallCheckResult \
                        and HardDifferenceSmallCheckResult \
                        and EqualityCheck\
                        and NumberResultsCheck\

    return CorrectnessCheck
























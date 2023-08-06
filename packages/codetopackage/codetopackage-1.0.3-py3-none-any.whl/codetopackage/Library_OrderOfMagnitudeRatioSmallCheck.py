"""
DESCRIPTION:
Returns true if every element in an array 
has an order of magnitude difference 
which is smaller than the maximum supplied


ARGS:
    A
    B
    Max

RETURNS:
    Good
        Type: Bool
        Description: True on good, False on Bad
"""
import numpy

from .Library_OrderOfMagnitudeRatio import Library_OrderOfMagnitudeRatio


def Library_OrderOfMagnitudeRatioSmallCheck(
    A = None, 
    B = None, 
    Max = None,
    PrintExtra = False,
    CheckArguments = True,
    ):

    if( CheckArguments):
        ArgumentErrorMessage = ""
        if (type(Max) != type(0.0) ):
            ArgumentErrorMessage += "type(Max) must be float. type(Max) ==   + "+str(type(Max))+"\n"
        #If any errors - terminate
        if ( len( ArgumentErrorMessage ) ):
            raise Exception( ArgumentErrorMessage)



    OrderOfMagnitudeRatio =  Library_OrderOfMagnitudeRatio(
        numpy.ndarray.flatten(numpy.array(A)), 
        numpy.ndarray.flatten(numpy.array(B)))

    if (PrintExtra):
        print('OrderOfMagnitudeRatio(s):', OrderOfMagnitudeRatio)
        print('Max Ratio Allowed:       ', Max)

    ResultType = type(OrderOfMagnitudeRatio)
    NumpyFloatType = type(numpy.float64(0.0))
    FloatType = type(0.0)
    IntType = type(0)

    #print 'ResultType', ResultType
    #print 'FloatType', FloatType
    #print 'NumpyFloatType', NumpyFloatType


    if (ResultType  != type(numpy.array([])) ):
        OrderOfMagnitudeRatio = numpy.array([OrderOfMagnitudeRatio])

    #print 'OrderOfMagnitudeRatio', OrderOfMagnitudeRatio



    Count = len(OrderOfMagnitudeRatio)

    Result  = True


    k = 0 
    while ( k <  Count):
        #print 'OrderOfMagnitudeRatio[k]', OrderOfMagnitudeRatio[k]
        if (OrderOfMagnitudeRatio[k] > Max):
            Result = False
        k = k  +1

    return Result














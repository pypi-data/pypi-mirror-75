"""
DESCRIPTION:
    #Takes two numbers, and compares their order of magnitude
    #To be used as a metric, we need to always have values of the same sign as inputs
    #We need to always order the inputs from low(abs(a), abs(b)) , high( abs(a), abs(b)
    #Result:
    #   Will always be positive
ARGS:
    A
        Type:
            Float 
            OR
            Array of floats

    B
        Type:
            Float 
            OR
            Array of floats

    CheckArguments    
    

RETURNS:
    OrderOfMagnitudeRatio


"""
import numpy


def Library_OrderOfMagnitudeRatio(
    A = None, 
    B = None, 
    CheckArguments = True
    ):

    #Cast each entry to a numpy array of floats
    Aarr = None
    Barr = None
    try:
        Aarr = numpy.array( A ).astype(numpy.float)
        Barr = numpy.array( B ).astype(numpy.float)
    except:
        print('A', A)
        print('B', B)
        return None



    if (Aarr.shape == ()):
        Aarr = numpy.array([Aarr])
    #print 'Aarr', Aarr.shape

    if (Barr.shape == ()):
        Barr = numpy.array([Barr])
    #print 'Barr', Barr.shape

    ElementwiseProduct = Aarr*Barr
    #print 'ElementwiseProduct', ElementwiseProduct

    if( CheckArguments):
        ArgumentErrorMessage = ""
        #Null Args:
        if (A is None):
            ArgumentErrorMessage += "(A is None)"
        if (B is None):
            ArgumentErrorMessage += "(B is None)"
        if (len(Aarr)!= len(Barr)):
            ArgumentErrorMessage += "(len(A)!= len(B))"


        #If any errors - terminate
        if ( len( ArgumentErrorMessage ) ):
            raise Exception( ArgumentErrorMessage)

    #Concatenate the two arrays, and make them vertical:
    AB = numpy.vstack((Aarr, Barr)).T
    #print 'AB', AB

    Result = []
    #Loop through the list of comparisons:
    for ab in AB:
        if (    #a              #b
                (ab[0] > 0 and  ab[1] > 0)
            or  (ab[0] < 0 and  ab[1] < 0)
            ):
            #Take the difference in the log
            Result.append( numpy.abs( numpy.log10(numpy.abs( ab[0])) - numpy.log10(numpy.abs( ab[1])) ) )
        elif (ab[0] == 0 and ab[1] == 0) : 
            Result.append( 0 )
        else:
            Result.append( float('Inf') )

        #print 'Result', Result
    Result = numpy.array(Result)

    #If only one value was passed in, then return that value instead of an array
    if (Result.shape[0] == 1):
        Result = Result[0]

    return Result

















"""
SOURCES

DESCRIPTION:

ARGS:

RESULTS:

TESTS:
"""
import numpy


def Library_HardDifferenceSmallCheck(
    A = None,
    B = None,
    Max = None,
    CheckArguments = True,
    PrintExtra = False,
    ):

    #Cast each entry to a numpy array of floats
    Aarr = numpy.array( A ).astype(numpy.float)
    Barr = numpy.array( B ).astype(numpy.float)

    if (Aarr.shape == ()):
        Aarr = numpy.array([Aarr])
    #print 'Aarr', Aarr.shape

    if (Barr.shape == ()):
        Barr = numpy.array([Barr])
    #print 'Barr', Barr.shape

    if( CheckArguments):
        ArgumentErrorMessage = ""
        #Null Args:
        if (A is None):
            ArgumentErrorMessage += "(A is None)"
        if (B is None):
            ArgumentErrorMessage += "(B is None)"
        if (len(Aarr)!= len(Barr)):
            ArgumentErrorMessage += "(len(A)!= len(B))\n"
            ArgumentErrorMessage += "  len(Aarr) =="  + str(len(Aarr)) + "\n"
            ArgumentErrorMessage += "  len(Barr) =="  + str(len(Barr)) + "\n"
        #If any errors - terminate
        if ( len( ArgumentErrorMessage ) ):
            raise Exception( ArgumentErrorMessage)


    HardDifferences = numpy.abs(Aarr - Barr)
    HardDifferenceSmallCheckResult = len( [i for i in numpy.ndarray.flatten(HardDifferences) if i > Max] ) == 0

    return HardDifferenceSmallCheckResult


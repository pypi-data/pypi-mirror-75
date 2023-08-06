"""
SOURCE:
    Mind of Douglas Adams
DESCRIPTION:
    Extracts the body of a library as a string
    Does not include header, or any material after the last return statement
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
    LibraryName
        Type:
            <type 'NoneType'>
        Description:
RETURNS:
    Result
        Type:
        Description:
"""
from .Library_FileReadAsText import Library_FileReadAsText
from .Library_StringSubstringFindAll import Library_StringSubstringFindAll

def Library_LibraryExtractBodyString(
    LibraryName= None,
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

    LibraryFilePath = LibraryName + '.py'

    LibraryText = Library_FileReadAsText( LibraryFilePath )

    TripleQuoteLocations = Library_StringSubstringFindAll(
        String = LibraryText, 
        Substring = "\"\"\"", 
    )


    if (len(TripleQuoteLocations) > 1):
        HeaderStartIndex = TripleQuoteLocations[0]
        HeaderEndIndex = TripleQuoteLocations[1]
        HeaderText = LibraryText[HeaderStartIndex + 3: HeaderEndIndex]
        if 'DESCRIPTION:' in HeaderText:
            BodyText = LibraryText[HeaderEndIndex + 3: -1]
            Result = BodyText
        else:
            Result = LibraryText
    else:
        Result = LibraryText


    return Result 










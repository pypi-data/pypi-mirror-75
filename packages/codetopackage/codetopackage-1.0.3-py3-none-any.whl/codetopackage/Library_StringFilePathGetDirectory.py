"""
SOURCE:
    Mind of Douglas Adams
DESCRIPTION:
    Extracts the directory from a full filepath
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
    FilePath
        Type:
            <type 'NoneType'>
        Description:
            None
RETURNS:
    Result
        Type:
        Description:
"""
import os
from .Library_StringSubstringFindAll import Library_StringSubstringFindAll
#-------------------------------------------------------------------------------
def Library_StringFilePathGetDirectory(
    FilePath = None,
    CheckArguments = True,
    PrintExtra = False,
    ):


    Result = None

    FilePath = os.path.realpath(FilePath)

    if (CheckArguments):
        ArgumentErrorMessage = ""

        FilePathPeriodIndexes = Library_StringSubstringFindAll(
            String = FilePath,  
            Substring = "\."
            )
        FilePathPeriodCount = len(  FilePathPeriodIndexes )

        if FilePathPeriodCount != 1 :
            ArgumentErrorMessage += 'Bad `FilePath` Arg.  FilePathPeriodCount is ' +  str(FilePathPeriodCount)+'\n' 

        if (len(ArgumentErrorMessage) > 0 ):
            if(PrintExtra):
                print("ArgumentErrorMessage:\n", ArgumentErrorMessage)
            raise Exception(ArgumentErrorMessage)




    FileStringSplit = FilePath.split('.')
    DirectoryFoldersSplit = FileStringSplit[0].split('/')
    Directory = "/".join( DirectoryFoldersSplit[0:-1] )
    #print 'Directory', Directory
    
        

    return Directory 
















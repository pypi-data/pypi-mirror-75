


"""
DESCRIPTION:
    Finds all the "imports" from a given library

    
    Interprets the from statements as . statments 

        i.e the following two statements should perform the same way:
            from A import B  ===  import A.B




ARGS:
    LibraryName:
        Type: python string
        Description:
            The name of the library, as if you were to include it in another libary
            e.g. `Library_ExampleLibraryGood`
            NOT A DIRECTORY`home/whatever/... /Library_ExampleLibraryGood.py`

            Assumes the current working directory contains the library

RETURNS:

"""
from .Library_LibraryExtractBodyString import Library_LibraryExtractBodyString

def Library_LibraryDependencyList(
    LibraryName = None,
    CheckArguments = True,
    PrintExtra = False,
    ):

    if (CheckArguments):
        ArgumentErrorMessage = ""
        if (len(ArgumentErrorMessage) > 0 ):
            if(PrintExtra):
                print("ArgumentErrorMessage:\n", ArgumentErrorMessage)
            raise Exception(ArgumentErrorMessage)


    #FileHandle = open(LibraryName + ".py", 'r')
    #FileLines = FileHandle.read().split('\n')

    FileText = Library_LibraryExtractBodyString( LibraryName = LibraryName)

    FileLines = FileText.split('\n')

    ImportLines = []
    for FileLine in FileLines:
        #        print FileLine[0:3]
        FileLine = FileLine.lstrip()
        if ( FileLine[0:5] == 'from ' ):
            if '#' in FileLine:
                FileLine=FileLine[:FileLine.find('#')]
            ImportLines.append(FileLine)
        if ( FileLine[0:7] == 'import '):
            if '#' in FileLine:
                FileLine=FileLine[:FileLine.find('#')]
            if ',' in FileLine:
                FileLine=FileLine[7:]
                for f in FileLine.split(','):
                    ImportLines.append('import '+f)
            else:
                ImportLines.append(FileLine)
            ImportLines.append(FileLine)

    ImportNames = []

    for ImportLine in ImportLines:
        if (PrintExtra):
            print('')
            print(ImportLine)
        ImportLineWords = ImportLine.split(' ')
        ImportLineWordCount = len(ImportLineWords)

        ImportLineParents = []
        ImportLineChildren = []

        FromWordIndex = -1
        ImportWordIndex = -1
        AsWordIndex = -1

        AsWordCount = 0
    
        k = 0
        while ( k <  ImportLineWordCount):
            Word = ImportLineWords[k]
            if (Word == 'from'):
                FromWordIndex = k
            elif (Word == 'import'):
                ImportWordIndex = k 
            elif (Word == 'as'):
                AsWordIndex = k
            else: #Word is either a parent or a child
                #FROM WORD FOUND:
                if ( FromWordIndex != -1 and ImportWordIndex == -1 and AsWordIndex == -1 ): 
                    #From found only
                    ImportLineParents.append(Word)
                if ( FromWordIndex != -1 and ImportWordIndex != -1 and AsWordIndex == -1 ): 
                    #From && Import found only
                    ImportLineChildren.append(Word)
                if ( FromWordIndex != -1 and ImportWordIndex != -1 and AsWordIndex != -1 ): 
                    #From && Import && As found only
                    AsWordCount += 1

                #NO FROM WORD FOUND:
                if ( FromWordIndex == -1 and ImportWordIndex != -1 and AsWordIndex == -1 ):
                    #Import found only 
                    ImportLineChildren.append(Word)
                if ( FromWordIndex == -1 and ImportWordIndex != -1 and AsWordIndex != -1 ):
                    #Import && As found only
                    AsWordCount += 1

            k = k + 1

        if (PrintExtra):
            print(' ImportWordIndex', ImportWordIndex)
            print(' FromWordIndex', FromWordIndex)
            print(' AsWordIndex', AsWordIndex)
            print(' ImportLineParent', ImportLineParents)
            print(' ImportLineChildren', ImportLineChildren)

        ImportParentsCount = len(ImportLineParents)
        ImportLineParent = None
        if ( ImportParentsCount == 0):
            ImportLineParent = ''
        elif ( ImportParentsCount == 1):
            ImportLineParent = ImportLineParents[0] + '.'
        elif ( ImportParentsCount > 1):
            print('LibraryName:', LibraryName)
            print('ImportLine', ImportLine)
            print('ImportLineParents', ImportLineParents)
            raise Exception


        ImportLineNames = []
        for ImportChild in ImportLineChildren:
            ImportLineNames.append( ImportLineParent + ImportChild )
        ImportNames =  ImportNames + ImportLineNames

    ImportNames = [s.strip(',') for s in ImportNames]

    ImportNames = [s.strip('\r') for s in ImportNames] #Don't know how this character shows up... but get rid of it

    return ImportNames
    








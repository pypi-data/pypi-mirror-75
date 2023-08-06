"""
SOURCE:
    Get list of VariableNames:
    http://stackoverflow.com/questions/30018977/how-can-i-get-a-list-of-the-symbols-in-a-sympy-expression

    Convert string into runable C-code
    https://github.com/neurophysik/jitcode/blob/master/jitcode/_jitcode.py
    http://stackoverflow.com/questions/42426967/create-usable-python-function-from-a-c-string-sympy-use-case

DESCRIPTION:

    Takes a sympy expression, and then turns it into a python callable function
    This is useful for when you have a function which is represented in the sympy notation for variaous manipulation,
    And then you want to run python things on it.
    I.E. you want to graph many values of it with matplotlib, or cram in many values with numpy

ARGS:
    SympyExpression
        Type:
            <type 'sympy.expr'>
        Description:
            Can have any number of free floating VariableNames
            e.g.    x + y  + z

    NewSympyFunctionDefaults
        Type: 
            <type 'dict'>
        Description:
            Has any subset of the Sympy Expressions Fre floating variables

    ReturnNative

        Type: 
            <type 'bool'>
        Description:
            The returned function takes math numbers as arguments and returns math numbers as results
            Should those number reuslts be cast back to native python complex values?
            ORRRR shoul dthose number results remain in sympy format?
            
            ReturnNative ==True -> returns complex math numbers which are readable by python

    FunctionConstructionMethod

RETURNS:

    PythonFunction
        Description:
            Python understood function which then expects all the free floating VariableNames as input
            e.g. 
                def PythonFunction( 
                    x, y, z 
                    ):
                    return expression(x=x, y=y, z=z)

            

        Type:
]           Python Lambda

"""
import copy
import inspect
import sympy
import sympy.printing
import sympy.utilities
import numpy
import scipy
import cffi
#-------------------------------------------------------------------------------
from .Library_CopyFunction import Library_CopyFunction
from .Type_Iterable import Type_Iterable
#-------------------------------------------------------------------------------
def Library_SympyExpressionToPythonFunction(
    SympyExpression = None,
    NewSympyFunctionDefaults = None,
    FloatPrecision = None,
    FunctionConstructionMethod = None, #TODO -> more!
    Method = None,
    ReturnNative = False,
    ReturnReal = False,
    PrintExtra = False,
    ):

    #Set arg defaults:
    if Method is not None and FunctionConstructionMethod is None:
        FunctionConstructionMethod = Method

    if FunctionConstructionMethod is None:
        FunctionConstructionMethod = 'lambdify'


    VariableNames = None
    #Figure out the sympy function defaults:
    VariableNameCount = 0
    VariableSymbols = SympyExpression.free_symbols
    if (NewSympyFunctionDefaults is None):

        #Get the VariableNames from the sympy expression:
        VariableNames = sorted([str(var) for var in SympyExpression.free_symbols])
        VariableNameCount = len(VariableNames)
        if (PrintExtra):
            print('VariableNameCount', VariableNameCount)
            print('VariableNames')
            print(VariableNames)
            
        #We copy the function with a set of None defaults using detected free parameters, 
        #   so that we have named VariableNames...    
        NewSympyFunctionDefaults = dict()
        for Variable in VariableNames:
            VariableName = str(Variable)
            if (PrintExtra):
                print('VariableName')
                print(VariableName)
            NewSympyFunctionDefaults[VariableName] = 0

    else:
        VariableNames = sorted(NewSympyFunctionDefaults.keys())
        VariableNameCount = len(VariableNames)

    if (PrintExtra):
        print('NewSympyFunctionDefaults')
        print(NewSympyFunctionDefaults)
    #print 'FloatPrecision', FloatPrecision
    if (PrintExtra): print('VariableNames', VariableNames)

    #Cast the expression into a python function:
    PythonFunction = None
    if (FunctionConstructionMethod == 'lambdify'):  #(WOOOOO -> This works as of 2017_05_16)

        #Construct the lambidfy function of the original expression:
        VariableSymbolsList = list(VariableSymbols)
        LambdifyFunction = sympy.lambdify(VariableSymbolsList, SympyExpression, modules='sympy')


        #Create a python wrapper function around the lambdify function
        #   The wrapper has default args, and thus is more robust
        #   This allows direct variable assignment with a very small speed cost
        #   Thus is in line with the `Functional Routine And Objective Data Coding Pattern`
        def PythonFunction( 
            *args, 
            **kwargs  
            ):

            #Construct a set of variable assignment tuples:
            if (PrintExtra): print('args', args)
            if (PrintExtra): print('kwargs', kwargs)
            ArgsCount = len(args)
            KwargsCount = len(kwargs)
            FunctionValueAssignments = copy.deepcopy(NewSympyFunctionDefaults)
            for VariableName, VariableNumber in zip(VariableNames, list(range(VariableNameCount))):
                VariableValue = None
                if (VariableNumber < ArgsCount):
                    VariableValue = args[VariableNumber]
                elif(VariableNumber < KwargsCount):
                    VariableValue = kwargs[VariableName]
                if (PrintExtra): print('---VariableValue', VariableValue)
                FunctionValueAssignments[VariableName] = VariableValue
            if (PrintExtra): print('FunctionValueAssignments', FunctionValueAssignments)
            FunctionSymbolValueAssignments = {}
            for VariableName, VariableValue in FunctionValueAssignments.items():
                FunctionSymbolValueAssignments[VariableName ] = VariableValue

            #Figure out which of the variables is valid in the lambdify expression:
            FinalArgSet = []
            for Symbol in VariableSymbolsList:
                SymbolName = str(Symbol)
                if SymbolName in FunctionSymbolValueAssignments:
                    SymbolValue = FunctionSymbolValueAssignments[SymbolName]
                    FinalArgSet.append(  SymbolValue )
                else:
                    FinalArgSet.append(sympy.Symbol( SymbolName))
            if (PrintExtra): print('FinalArgSet', FinalArgSet)

            #Deal with when a point is passed in like [2,3,4]: #FIXME: make more robust
            if len(args) > 0 and Type_Iterable( args[0] ):
                FinalArgSet = args[0]
            if len(kwargs) > 0 and Type_Iterable( list(kwargs.values())[0] ):
                FinalArgSet = list(kwargs.values())[0]

            ReturnValue = LambdifyFunction( *FinalArgSet   )



            #If the result is numerical, cast it to native python number:
            if (ReturnNative):
                ReturnValue = complex(ReturnValue)

            if ReturnValue == sympy.nan:
                ReturnValue = None

            if (ReturnReal):
                ReturnValue = numpy.real(ReturnValue).astype(numpy.float64)

            return ReturnValue

        #$raise Exception('TODO - lambdify')

    elif (FunctionConstructionMethod == 'ccode'): 
        #TODO See -> jitcode
        ExpressionCCode = sympy.printing.ccode(SympyExpression)
        #many options here... they are all bad
        print('ExpressionCCode')
        print(ExpressionCCode)
        raise Exception('TODO - ccode')

    elif (FunctionConstructionMethod == 'evalf'): 
        def PythonFunction( 
            *args, 
            **kwargs  
            ):


            #Construct a set of variable assignment tuples:
            if (PrintExtra): print('args', args)
            if (PrintExtra): print('kwargs', kwargs)
            ArgsCount = len(args)
            KwargsCount = len(kwargs)
            FunctionValueAssignments = copy.deepcopy(NewSympyFunctionDefaults)
            for VariableName, VariableNumber in zip(VariableNames, list(range(VariableNameCount))):
                VariableValue = None
                if (VariableNumber < ArgsCount):
                    VariableValue = args[VariableNumber]
                elif(VariableNumber < KwargsCount):
                    VariableValue = kwargs[VariableName]
                if (PrintExtra): print('---VariableValue', VariableValue)
                FunctionValueAssignments[VariableName] = VariableValue
            if (PrintExtra): print('FunctionValueAssignments', FunctionValueAssignments)
            FunctionSymbolValueAssignments = {}
            for VariableName, VariableValue in FunctionValueAssignments.items():
                FunctionSymbolValueAssignments[sympy.Symbol(VariableName) ] = VariableValue


            #print 'SympyExpression', SympyExpression
            #Plug in the variable assignemtns into the expression:
            SympyExpressionSubs = SympyExpression.subs(
                FunctionSymbolValueAssignments
                )
            #print 'SympyExpressionSubs', SympyExpressionSubs

            #Handle special result cases:
            if SympyExpressionSubs == sympy.nan:
                ReturnValue = None

            else:
                ReturnValue = SympyExpressionSubs.evalf(
                    FloatPrecision, 
                    #subs=FunctionSymbolValueAssignments
                    ) #Evalf is really slow...


            #print 'ReturnValue', ReturnValue
            if (ReturnNative):
                ReturnValue = complex(ReturnValue)

            return ReturnValue



    #Be able to handle array of points as arguements
    def ArrayHandlePythonFunction(*args, **kwargs):
        return PythonFunction(*args, **kwargs)

    return PythonFunction






    #Why didn't I make a deep copy? (of the returned function)
    #   seems logical to make a deep copy 
    #   to allow for passing around the function as an argrument 
    #   and allow for parallelism
    # --> figureed out why 2016_05_31 -> 
    #   Because you can always make a deep copy after calling this method, 
    #   and the overhead is slower
    """
    #Make a copy of the new python function with new defaults:
    PythonFunctionNamedArgs = Library_CopyFunction.Main( 
        Function = PythonFunction, 
        NewName = 'SympyFunctionNamedArgs',
        NewDefaults = NewSympyFunctionDefaults ,
        PrintExtra = PrintExtra,
        )
    return PythonFunctionNamedArgs
    """



















"""

SOURCE:
http://docs.sympy.org/dev/modules/parsing.html

DESCRIPTION:

    Takes a string expression, like one you would throw at google,
    Returns a sympy expression which can then be picked appart and make use of various pythonic things

ARGS:
    StringExpression
        Type: Python String

RETURNS:
    SympyExpression
        Type: sympy expression

"""

import sympy
import sympy.parsing.sympy_parser #Requires second import for unknown reason

from .Type_SympyExpression import Type_SympyExpression
#def StringExpressionToSympyExpression(
def Library_StringExpressionToSympyExpression(
    StringExpression = None,
    ):

    #print 'String Cast Trigger'
    #print 'start->', StringExpression

    SympyExpression = None
    if isinstance(StringExpression, str):
        #NOTE:
        #   WOWWWWWW -> THIS WAS SO ANNOYING I WASTED 4 HOURS ON THIS
        #   Sympy native string casts.... will create an inf in python
        #   Casting inf from a string, will be treated as a variable in a sympy expression
        #   so this extra line of code, properly treats the word   inf    as infinity in sympy.
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        StringExpression = StringExpression.replace('inf', 'oo') 
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        SympyExpression = sympy.parsing.sympy_parser.parse_expr(StringExpression, evaluate=False) #<---- THIS IS THE ONLY PLACE IN THE CODE BASE WHERE THIS FUNCTION SHOULD EXIST
    else:
        raise Exception('StringExpression is bs type')

    #print 'end->', SympyExpression
    return SympyExpression







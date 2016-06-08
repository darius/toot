"Convert Toot programs from concrete syntax to abstract syntax."

import operator

from parson import Grammar
from abstract_syntax import *

toot_grammar = r""" program.

program: _ defn* :hug print :end                 :Program.
print:   'print'__ exp.
defn:    'def'__ id '('_ params ')'_ ':'_ stmt   :Definition.
stmt:    'return'__ exp.

exp:     exp1 ('if'__ exp1 'else'__ exp :If)?.
exp1:    exp2 ( '<'_   exp2 :Less
              | '=='_  exp2 :Eq)?.
exp2:    exp3 (  '+'_  exp3 :Add
               | '-'_  exp3 :Sub)*.
exp3:    exp4 (  '*'_  exp4 :Mul
               | '/'_  exp4 :Div
               | '%'_  exp4 :Mod)*.

exp4:    '('_ exp ')'_
      |  '-'_ exp4              :Neg
      |  id '('_ arguments ')'_ :Call
      |  id                     :Variable
      |  /(\d+)/_          :int :Constant.

params:     id ** (','_)        :hug.
arguments:  exp1 ** (','_)      :hug.

id = /([A-Za-z_][A-Za-z_0-9]*)\b/_.
_  = /\s*/.
__ = /\b/_.
"""

def make_prim2(fn):
    return lambda arg1, arg2: Prim2(fn, arg1, arg2)

Less = make_prim2(operator.lt)
Eq   = make_prim2(operator.eq)
Add  = make_prim2(operator.add)
Sub  = make_prim2(operator.sub)
Mul  = make_prim2(operator.mul)
Div  = make_prim2(operator.truediv)
Mod  = make_prim2(operator.mod)
Neg  = lambda expr: Sub(Constant(0), expr)

parse_toot = Grammar(toot_grammar)(**globals())

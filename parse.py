"Convert Toot programs from concrete syntax to abstract syntax."

from parson import Grammar
import abstract_syntax

toot_grammar = r""" program :end.

program: defn* :hug print                   :Program.
print:   "print" exp.
defn:    "def" id '(' params ')' ':' stmt   :Definition.
stmt:    "return" exp.

exp:     exp1 ("if" exp1 "else" exp :If)?.
exp1:    exp2 ( '<'   exp2 :Less
              | '=='  exp2 :Eq  )?.
exp2:    exp3 (  '+'  exp3 :Add
               | '-'  exp3 :Sub )*.
exp3:    exp4 (  '*'  exp4 :Mul
               | '/'  exp4 :Div
               | '%'  exp4 :Mod )*.

exp4:    '(' exp ')'
      |  '-' exp4             :Neg
      |  id '(' arguments ')' :Call
      |  id                   :Variable
      |  /(\d+)/         :int :Constant.

params:     id ** ','         :hug.
arguments:  exp1 ** ','       :hug.

id:      /([A-Za-z_][A-Za-z_0-9]*)/.

FNORD ~: /\s*/.
"""

parse_toot = Grammar(toot_grammar).bind(abstract_syntax)

"""
Convert Toot programs from concrete syntax to abstract syntax.
"""

from parson import Grammar, hug
import absyntax

toot_grammar = Grammar(r"""
program: _ defn* :hug print !/./                  :Program.
print:   /print\b/_ exp.
defn:    /def\b/_ id '('_ params ')'_ ':'_ stmt   :Definition.
stmt:    /return\b/_ exp.

exp:     exp1 (/if\b/_ exp1 /else\b/_ exp :If)?.
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

params:     (id (','_ id)*)?     :hug.
arguments:  (exp1 (','_ exp1)*)? :hug.

id = /([A-Za-z_][A-Za-z_0-9]*)\b/_.
_ = /\s*/.
""")(hug=hug, **absyntax.__dict__)

parse_toot = toot_grammar.program

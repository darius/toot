"""
A warmup: filling in template strings.

Glossary: t for template, env for environment
"""

eg_template = "To understand $x you must first understand @y."
eg_env = {'x': 'recursion',
          'y': ['base cases', 'recursion']}

## fill(eg_template, eg_env)
#. 'To understand recursion you must first understand base cases and recursion.'

def fill(t, env):
    if   t == '':     return ''
    elif t[0] == '$': return env[t[1]]               + fill(t[2:], env)
    elif t[0] == '@': return ' and '.join(env[t[1]]) + fill(t[2:], env)
    else:             return t[0]                    + fill(t[1:], env)

"""Now separate 'compile time' from 'run time': at 'compile time' we
know only the template, and at run time we also know the env. In the 
first version of this we put off all the work till run time:"""

## filler = make_filler(eg_template)
## filler(eg_env)
#. 'To understand recursion you must first understand base cases and recursion.'

def make_filler(t):
    if   t == '':     return lambda env: ''
    elif t[0] == '$': return lambda env:               env[t[1]] + make_filler(t[2:])(env)
    elif t[0] == '@': return lambda env: ' and '.join(env[t[1]]) + make_filler(t[2:])(env)
    else:             return lambda env:                    t[0] + make_filler(t[1:])(env)

"Now eagerly do what we can at 'compile time':"

def make_filler(t):
    if   t == '':     return Empty
    elif t[0] == '$': return Hole    (t[1], make_filler(t[2:]))
    elif t[0] == '@': return ListHole(t[1], make_filler(t[2:]))
    else:             return Constant(t[0], make_filler(t[1:]))

Empty =                              lambda env: ''
def Hole    (name, sequel):   return lambda env:               env[name] + sequel(env)
def ListHole(name, sequel):   return lambda env: ' and '.join(env[name]) + sequel(env)
def Constant(string, sequel): return lambda env:                  string + sequel(env)

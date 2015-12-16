"A recursive interpreter."
# t:   tree node
# dd:  dict of definitions
# env: environment mapping variables to values

import absyntax as A

def eval_program(program):
    return program.expr.eval({defn.name: defn for defn in program.defns},
                             empty_env)

A.Constant.eval = lambda t, dd, env: t.value
A.Variable.eval = lambda t, dd, env: fetch(env, t.name)
A.If      .eval = lambda t, dd, env: (t.then.eval(dd, env) if t.test.eval(dd, env)
                                     else t.else_.eval(dd, env))
A.Call    .eval = lambda t, dd, env: eval_call(t, dd, env)
A.Prim2   .eval = lambda t, dd, env: t.op(t.arg1.eval(dd, env),
                                          t.arg2.eval(dd, env))

def eval_call(t, dd, env):
    defn = dd[t.name]
    operands = tuple(argument.eval(dd, env) for argument in t.arguments)
    return defn.expr.eval(dd, make_env(defn.params, operands))

empty_env = {}

def make_env(names, values):
    return dict(zip(names, values))

def fetch(env, name):
    return env[name]

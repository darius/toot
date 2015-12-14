"""
Like first_terp, but with the environments represented differently:
instead of a dict, each environment is a pair (names, values).
"""

import absyntax as A

def eval_program(program):
    return program.expr.eval(make_env((), ()),
                             make_env(tuple(defn.name for defn in program.defns),
                                      program.defns))

A.Constant.eval = lambda t, vr, fr: t.value
A.Variable.eval = lambda t, vr, fr: fetch(vr, t.name)
A.If      .eval = lambda t, vr, fr: (t.then.eval(vr, fr) if t.test.eval(vr, fr)
                                     else t.else_.eval(vr, fr))
A.Call    .eval = lambda t, vr, fr: eval_call(t, vr, fr)
A.Prim2   .eval = lambda t, vr, fr: t.op(t.arg1.eval(vr, fr),
                                         t.arg2.eval(vr, fr))

def eval_call(t, vr, fr):
    defn = fetch(fr, t.name)
    operands = [argument.eval(vr, fr) for argument in t.arguments]
    return defn.expr.eval(make_env(defn.params, operands), fr)

def make_env(names, values):
    return (names, values)

def fetch(env, name):
    (names, values) = env
    return values[names.index(name)]

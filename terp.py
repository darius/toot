"""
A recursive interpreter.
"""

import absyntax as A

def eval_program(program):
    return program.expr.eval({}, {defn.name: defn
                                  for defn in program.defns})

A.Constant.eval = lambda t, vr, fr: t.value
A.Variable.eval = lambda t, vr, fr: vr[t.name]
A.If      .eval = lambda t, vr, fr: (t.then.eval(vr, fr) if t.test.eval(vr, fr) else
                                     t.else_.eval(vr, fr))
A.Call    .eval = lambda t, vr, fr: eval_call(t, vr, fr)
A.Prim2   .eval = lambda t, vr, fr: t.op(t.arg1.eval(vr, fr),
                                         t.arg2.eval(vr, fr))

def eval_call(t, vr, fr):
    defn = fr[t.name]
    operands = [argument.eval(vr, fr) for argument in t.arguments]
    return defn.expr.eval(dict(zip(defn.params, operands)), fr)

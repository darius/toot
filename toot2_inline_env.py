"Pass the static and dynamic parts of the environment around separately."
# t:      tree node
# dd:     dict of definitions
# vn, vv: variable names, variable values

import abstract_syntax as A

def eval_program(program):
    return program.expr.eval({defn.name: defn for defn in program.defns}, (), ())

A.Constant.eval = lambda t, dd, vn, vv: t.value
A.Variable.eval = lambda t, dd, vn, vv: vv[vn.index(t.name)]
A.If      .eval = lambda t, dd, vn, vv: (t.then.eval(dd, vn, vv) if t.test.eval(dd, vn, vv)
                                         else t.else_.eval(dd, vn, vv))
A.Call    .eval = lambda t, dd, vn, vv: eval_call(t, dd, vn, vv)
A.Prim2   .eval = lambda t, dd, vn, vv: t.op(t.arg1.eval(dd, vn, vv),
                                             t.arg2.eval(dd, vn, vv))

def eval_call(t, dd, vn, vv):
    defn = dd[t.name]
    operands = tuple(argument.eval(dd, vn, vv) for argument in t.arguments)
    return defn.expr.eval(dd, defn.params, operands)

"Change to a staged interface: the first stage returns a function that's the second stage."
# t:      tree node
# dd:     dict of definitions
# vn, vv: variable names, variable values

import abstract_syntax as A

def eval_program(program):
    do_expr = program.expr.eval({defn.name: defn for defn in program.defns}, ())
    return do_expr(())

A.Constant.eval = lambda t, dd, vn: lambda vv: t.value
A.Variable.eval = lambda t, dd, vn: lambda vv: vv[vn.index(t.name)]
A.If      .eval = lambda t, dd, vn: lambda vv: (t.then.eval(dd, vn)(vv) if t.test.eval(dd, vn)(vv)
                                                else t.else_.eval(dd, vn)(vv))
A.Call    .eval = lambda t, dd, vn: lambda vv: eval_call(t, dd, vn)(vv)
A.Prim2   .eval = lambda t, dd, vn: lambda vv: t.op(t.arg1.eval(dd, vn)(vv),
                                                    t.arg2.eval(dd, vn)(vv))

def eval_call(t, dd, vn):
    def do_call(vv):
        defn = dd[t.name]
        operands = tuple(argument.eval(dd, vn)(vv) for argument in t.arguments)
        return defn.expr.eval(dd, defn.params)(operands)
    return do_call

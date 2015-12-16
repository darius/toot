"Push the 'analysis' work back into the first stage (and rename it to 'analyze')."
# t:      tree node
# dd:     dict of definitions
# vn, vv: variable names, variable values

import abstract_syntax as A

def eval_program(program):
    do_expr = program.expr.analyze({defn.name: defn for defn in program.defns}, ())
    return do_expr(())

A.Constant.analyze = lambda t, dd, vn: lambda vv: t.value
A.Variable.analyze = lambda t, dd, vn: do_variable(vn.index(t.name))
A.If      .analyze = lambda t, dd, vn: do_if(t.then.analyze(dd, vn),
                                             t.test.analyze(dd, vn),
                                             t.else_.analyze(dd, vn))
A.Call    .analyze = lambda t, dd, vn: analyze_call(t, dd, vn)
A.Prim2   .analyze = lambda t, dd, vn: do_prim2(t.op,
                                                t.arg1.analyze(dd, vn),
                                                t.arg2.analyze(dd, vn))

def analyze_call(t, dd, vn):
    defn = dd[t.name]
    arguments = [argument.analyze(dd, vn) for argument in t.arguments]
    def do_call(vv):
        operands = tuple(argument(vv) for argument in arguments)
        callee = defn.expr.analyze(dd, defn.params)
        return callee(operands)
    return do_call

def do_variable(index):       return lambda vv: vv[index]
def do_if(then, test, else_): return lambda vv: (then(vv) if test(vv) else else_(vv))
def do_prim2(op, arg1, arg2): return lambda vv: op(arg1(vv), arg2(vv))

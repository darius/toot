"I lied: we were still analyzing the definitions at call time. Let's do them eagerly too."
# t:      tree node
# dd:     dict of *analyzed* definitions
# vn, vv: variable names, variable values
# dn, dv: definition names, definition values (i.e. analyzed definitions)

import absyntax as A

def eval_program(program):
    dn = tuple(defn.name for defn in program.defns)
    dv = tuple(defn.expr.analyze(dn, defn.params) for defn in program.defns)
    do_expr = program.expr.analyze(dn, ())
    return do_expr(dv, ())

A.Constant.analyze = lambda t, dn, vn: do_constant(t.value)
A.Variable.analyze = lambda t, dn, vn: do_variable(vn.index(t.name))
A.If      .analyze = lambda t, dn, vn: do_if(t.then.analyze(dn, vn),
                                             t.test.analyze(dn, vn),
                                             t.else_.analyze(dn, vn))
A.Call    .analyze = lambda t, dn, vn: do_call(dn.index(t.name),
                                               tuple(argument.analyze(dn, vn)
                                                     for argument in t.arguments))
A.Prim2   .analyze = lambda t, dn, vn: do_prim2(t.op,
                                                t.arg1.analyze(dn, vn),
                                                t.arg2.analyze(dn, vn))

def do_constant(value):               return lambda dv, vv: value
def do_variable(index):               return lambda dv, vv: vv[index]
def do_if(do_then, do_test, do_else): return lambda dv, vv: do_then(dv, vv) if do_test(dv, vv) else do_else(dv, vv)
def do_prim2(op, do_arg1, do_arg2):   return lambda dv, vv: op(do_arg1(dv, vv), do_arg2(dv, vv))

def do_call(defn_index, do_arguments):
    def result(dv, vv):
        callee = dv[defn_index]
        operands = tuple(do_argument(dv, vv) for do_argument in do_arguments)
        return callee(dv, operands)
    return result

"Instead of passing and returning values, push and pop them on a stack."
# t:      tree node
# dn, dv: definition names, definition values (i.e. analyzed definitions)
# vn, vv: variable names, variable values

import absyntax as A

def eval_program(program):
    dn = tuple(defn.name for defn in program.defns)
    dv = tuple(defn.expr.analyze(dn, defn.params) for defn in program.defns)
    do_expr = program.expr.analyze(dn, ())
    stack = []
    do_expr(dv, (), stack)
    return stack.pop()

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

def do_constant(value):
    def result(dv, vv, stack):
        stack.append(value)
    return result

def do_variable(index):
    def result(dv, vv, stack):
        stack.append(vv[index])
    return result

def do_if(do_then, do_test, do_else):
    def result(dv, vv, stack):
        do_test(dv, vv, stack)
        test_value = stack.pop()
        if test_value: do_then(dv, vv, stack)
        else:          do_else(dv, vv, stack)
    return result

def do_prim2(op, do_arg1, do_arg2):
    def result(dv, vv, stack):
        do_arg1(dv, vv, stack)
        do_arg2(dv, vv, stack)
        arg2 = stack.pop()
        arg1 = stack.pop()
        stack.append(op(arg1, arg2))
    return result

def do_call(defn_index, do_arguments):
    def result(dv, vv, stack):
        callee = dv[defn_index]
        for do_argument in do_arguments:
            do_argument(dv, vv, stack)
        operands = stack[-len(do_arguments):]
        stack[-len(do_arguments):] = []
        callee(dv, operands, stack)
    return result

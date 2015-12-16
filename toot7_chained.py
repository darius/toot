"Represent the analyzed program as a list of instructions."
# t:      tree node
# dd:     dict of *analyzed* definitions
# vn, vv: variable names, variable values
# dn, dv: definition names, definition values (i.e. analyzed definitions)

import absyntax as A

def eval_program(program):
    dn = tuple(defn.name for defn in program.defns)
    dv = tuple(defn.expr.analyze(dn, defn.params) for defn in program.defns)
    do_expr = program.expr.analyze(dn, ())
    return run(do_expr, dv, ())

def run(instructions, dv, vv):
    stack = []
    pc = 0
    while pc < len(instructions):
        pc += instructions[pc](dv, vv, stack)
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
    def push_constant(dv, vv, stack):
        stack.append(value)
        return 1
    return (push_constant,)

def do_variable(index):
    def push_variable(dv, vv, stack):
        stack.append(vv[index])
        return 1
    return (push_variable,)

def do_if(do_then, do_test, do_else):
    def branch(dv, vv, stack):
        test_value = stack.pop()
        if test_value: return 1
        else:          return 1 + len(do_then) + 1
    def goto(dv, vv, stack):
        return 1 + len(do_else)
    return do_test + (branch,) + do_then + (goto,) + do_else

def do_prim2(op, do_arg1, do_arg2):
    def do_op(dv, vv, stack):
        arg2 = stack.pop()
        arg1 = stack.pop()
        stack.append(op(arg1, arg2))
        return 1
    return do_arg1 + do_arg2 + (do_op,)

def do_call(defn_index, do_arguments):
    def call(dv, vv, stack):
        callee = dv[defn_index]
        operands = stack[-len(do_arguments):]
        stack[-len(do_arguments):] = []
        stack.append(run(callee, dv, operands))
        return 1
    return sum(do_arguments, ()) + (call,)

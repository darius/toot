"Represent the instructions as data instead of closures."
# t:      tree node
# dn, dv: definition names, definition values (i.e. analyzed definitions)
# vn, vv: variable names, variable values

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
        pc += step(instructions[pc], dv, vv, stack)
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

def step(instruction, dv, vv, stack):
    opcode, operand = instruction
    if   opcode == push_constant:
        stack.append(operand)
        return 1
    elif opcode == push_variable:
        stack.append(vv[operand])
        return 1
    elif opcode == branch:
        test_value = stack.pop()
        if test_value: return 1
        else:          return 1 + operand
    elif opcode == goto:
        return 1 + operand
    elif opcode == do_op:
        arg2 = stack.pop()
        arg1 = stack.pop()
        stack.append(operand(arg1, arg2))
        return 1
    elif opcode == call:
        defn_index, narguments = operand
        callee = dv[defn_index]
        arguments = stack[-narguments:]
        stack[-narguments:] = []
        stack.append(run(callee, dv, arguments))
        return 1
    else:
        assert False

def do_constant(value):
    return ((push_constant, value),)

def do_variable(index):
    return ((push_variable, index),)

def do_if(do_then, do_test, do_else):
    return do_test + ((branch, len(do_then)+1),) + do_then + ((goto, len(do_else)),) + do_else

def do_prim2(op, do_arg1, do_arg2):
    return do_arg1 + do_arg2 + ((do_op, op),)

def do_call(defn_index, do_arguments):
    return sum(do_arguments, ()) + ((call, (defn_index, len(do_arguments))),)

push_constant, push_variable, branch, goto, do_op, call = range(6)

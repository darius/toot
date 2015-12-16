"n * factorial(n - 1)"
# ==>
#    Parsed code (AST)                  Instructions            Stack in an example run, n=5
Prim2(operator.mul,                                             []
      Variable('n'),                    push_variable 0         [5]
      Call('factorial',
           (Prim2(operator.sub,
                  Variable('n'),        push_variable 0         [5, 5]
                  Constant(1)),)))),)   push_constant 1         [5, 5, 1]
                                        do_op2 operator.sub     [5, 4]
                                        call (0, 1)             [5, 24]
                                        do_op2 operator.mul     [120]

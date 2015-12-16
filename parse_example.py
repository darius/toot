"n * factorial(n - 1)"
# ==>
Prim2(operator.mul,
      Variable('n'),
      Call('factorial',
           (Prim2(operator.sub,
                  Variable('n'),
                  Constant(1)),)))),)

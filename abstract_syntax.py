"""
Abstract syntax trees for Toot programs.
"""

def make_ast_type(spec):
    type_name, rhs = spec.split(':')
    names = rhs.split()

    def __init__(self, *args):
        assert len(args) == len(names), ("arguments don't match #params: %r vs. %r"
                                         % (args, names))
        self.__dict__.update(zip(names, args))

    def __repr__(self):
        return '%s(%s)' % (type_name, ', '.join(repr(getattr(self, name))
                                                for name in names))

    return type(type_name, (), {
        '__init__': __init__,
        '__repr__': __repr__,
    })

Program    = make_ast_type('Program: defns expr')
Definition = make_ast_type('Definition: name params expr')

Constant   = make_ast_type('Constant: value')
Variable   = make_ast_type('Variable: name')
If         = make_ast_type('If: then test else_')
Call       = make_ast_type('Call: name arguments')
Prim2      = make_ast_type('Prim2: op arg1 arg2')

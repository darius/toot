"""
Smoke test
"""

from parse import parse_toot
from terp import eval_program

def run(program_text):
    program, = parse_toot(program_text)
    return eval_program(program)

## run(open('factorial.toot').read())
#. 120

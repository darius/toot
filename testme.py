"""
Smoke test
"""

from parse import parse_toot
import terp0 as terp

def run(program_text):
    program, = parse_toot(program_text)
    return terp.eval_program(program)

## run(open('factorial.toot').read())
#. 120

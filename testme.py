"""
Smoke test
"""

from parse import parse_toot
#import terp0 as terp
#import terp1_split_env as terp
#import terp2_inline_env as terp
#import terp3_staged_env as terp
#import terp4_eagerly_analyze as terp
import terp5_eager_all_the_way as terp

def run(program_text):
    program, = parse_toot(program_text)
    return terp.eval_program(program)

## run(open('factorial.toot').read())
#. 120

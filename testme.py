"Smoke test."

from parse import parse_toot

#import toot0 as toot
#import toot1_split_env as toot
#import toot2_inline_env as toot
#import toot3_staged_env as toot
#import toot4_eagerly_analyze as toot
#import toot5_eager_all_the_way as toot
#import toot6_stacky as toot
#import toot7_chained as toot
import toot8_encoded as toot

def run(program_text):
    program, = parse_toot(program_text)
    return toot.eval_program(program)

print run(open('factorial.toot').read())
#. 120

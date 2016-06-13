# toot

I gave a talk on transforming a simple interpreter into a bytecode
compiler, showing an example in Python.

[outline.text](https://github.com/darius/toot/blob/master/outline.text)
gives the first 10 minutes; after that I winged it more, going through
[the slides](https://github.com/darius/toot/blob/master/slideshow.el).

As a talk it was a failure: lecturing for an hour on technical details
asks a lot of an audience. It might still be of interest as a small
example of compiling to explore on your own, if you're comfortable
with recursion and higher-order functions.

For a warmup we take a [string template
language](https://github.com/darius/toot/blob/master/template.py) and
transform the interpreter to move some of its work to 'compile' time.

For the main course we interpret a tiny subset of Python ([example
program](https://github.com/darius/toot/blob/master/factorial.toot))
and gradually go from
[interpreter](https://github.com/darius/toot/blob/master/toot0.py) to
[bytecode
compiler](https://github.com/darius/toot/blob/master/toot8_encoded.py).

This was most influenced by the compiling chapter of [Essentials of
Programming Languages](http://www.eopl3.com/), first edition; I think
the latest edition dropped it, though it still has a lot to say about
transforming programs in stages.

from pathlib import Path

from wardoff.analyzers import syntax


def tokenizer(given_input, trim=False):
    code = None
    infile = None
    line = None
    try:
        infile, line = given_input.split("+")
    except ValueError:
        # here we consider that we are in the "to many value to unpack"
        # situation and so that user passed raw code to tokenize
        code = given_input
    finally:
        if not code and Path(infile).is_file():
            with open(infile) as fp:
                lines = fp.readlines()
            # file start at line 1 while list start at index 0
            line_position = int(line) - 1
            code = lines[line_position]
        if trim:
            code = code.strip()
        return syntax.tokenizer(code)

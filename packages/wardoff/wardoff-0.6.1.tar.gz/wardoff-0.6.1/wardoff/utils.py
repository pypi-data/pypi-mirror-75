import os
from pathlib import Path


def identifier():
    return "wardoff-{pid}".format(pid=os.getpid())


def get_pyfiles(path):
    return sorted(Path(path).glob("**/*.py"))

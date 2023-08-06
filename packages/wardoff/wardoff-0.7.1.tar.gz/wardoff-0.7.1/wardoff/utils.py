import os
from pathlib import Path


def identifier(name=None, prefix="wardoff-"):
    if not name:
        name = str(os.getpid())
    if name.startswith("wardoff-") and prefix.startswith("wardoff-"):
        name.replace("wardoff-", "")
    return f"{prefix}{name}"


def get_pyfiles(path):
    return sorted(Path(path).glob("**/*.py"))

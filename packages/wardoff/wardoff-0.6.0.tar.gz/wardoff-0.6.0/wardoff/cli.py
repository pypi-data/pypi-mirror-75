import argparse
import textwrap
from pathlib import Path

from wardoff.analyzers import module as module_analyzer

VALID_VERSIONS = [
    "2",
    "2.6",
    "2.7",
    "3",
    "3.1",
    "3.2",
    "3.3",
    "3.4",
    "3.5",
    "3.6",
    "3.7",
    "3.8",
    "3.9",
]


class ProjectType:
    def __call__(self, string):
        try:
            if not string or string == ".":
                return module_analyzer.PathAnalyzer(".")
            if Path(string).is_file():
                return module_analyzer.FileAnalyzer(string)
            if Path(string).is_dir():
                return module_analyzer.PathAnalyzer(".")
            if string.startswith("http") or string.startswith("git"):
                return module_analyzer.RepoAnalyzer(string)
            # By default we consider the passed argument as a pypi project name
            return module_analyzer.PackageAnalyzer(string)
        except module_analyzer.ModuleAnalyzerInitializationError as err:
            print(err)


class VersionType:
    def __call__(self, string):
        versions = string.split(",")
        if not isinstance(versions, list):
            versions = [versions]
        if not set(versions).issubset(set(VALID_VERSIONS)):
            print(
                "Version not recognized (choose from {ver})".format(
                    ver=",".join([f"'{el}'" for el in VALID_VERSIONS])
                )
            )
        return versions


def common_cli(func):
    def wrapper():
        parser = func()
        parser.add_argument(
            "-v",
            "--verbosity",
            action="count",
            help="increase output verbosity",
            default=0,
        )
        parser.add_argument(
            "-k",
            "--keep-env",
            action="store_true",
            help="don't remove the generated virtual env if option is passed.",
        )
        return parser

    return wrapper


@common_cli
def infos():
    parser = argparse.ArgumentParser(
        description="Show infos about all the project's requirements",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "project",
        nargs="?",
        type=ProjectType(),
        default=".",
        help="Path, file, package, or distant "
        "repo to analyze. "
        "If not provided the current dir will be analyzed.",
    )
    parser.add_argument(
        "--no-classifiers",
        action="store_true",
        help="pypi classifiers will not been displayed.",
    )
    parser.add_argument(
        "--filter", nargs="?", help="filtered details' fields",
    )
    parser.add_argument(
        "--no-separator",
        action="store_true",
        help="display a separator between detailed results",
    )
    parser.add_argument(
        "--no-key", action="store_true", help="display the details' keys",
    )
    parser.add_argument(
        "--support",
        nargs="?",
        type=VersionType(),
        help="only display requirements who support the given python "
        "versions (allowed values: {ver})".format(
            ver=",".join([f"'{el}'" for el in VALID_VERSIONS])
        ),
    )
    return parser


@common_cli
def freeze():
    parser = argparse.ArgumentParser(
        description="Freeze requirements of a given project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "project",
        nargs="?",
        type=ProjectType(),
        default=".",
        help="Path, file, package, or distant "
        "repo to analyze. "
        "If not provided the current dir will be analyzed.",
    )
    return parser


@common_cli
def main():
    parser = argparse.ArgumentParser(
        description="Find deprecations in your requirements and "
        "underlying libraries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "project",
        nargs="?",
        type=ProjectType(),
        default=".",
        help="Path, file, package, or distant \
                        repo to analyze. \
                        If not provided the current dir will be analyzed.",
    )
    return parser


@common_cli
def tokenizer():
    epilog = textwrap.dedent(
        """\
        This command can be used to transform raw code in python
        tokens. It could be useful for debuging or testing purpose.
        It is a bit similar to the stdlib tokenzier module [1]
        but here you can tokenize code from the stdin and not only
        from a file.
        [1] https://docs.python.org/3/library/tokenize.html#command-line-usage
    """
    )
    parser = argparse.ArgumentParser(
        description="Tokenize code python code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog,
    )
    parser.add_argument(
        "-t",
        "--trim",
        action="store_true",
        default=False,
        help="trim whitespaces if flag is given",
    )
    parser.add_argument(
        "code",
        help="Code to tokenize, could be raw code or a specific "
        "line of file to analyze (e.g /path/to/file+12 where +12 is the "
        "line number to tokenize)",
    )
    return parser

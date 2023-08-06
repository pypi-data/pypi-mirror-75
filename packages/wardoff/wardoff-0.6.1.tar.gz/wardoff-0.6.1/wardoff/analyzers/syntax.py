import ast
import io
import tokenize
from pathlib import Path

from wardoff import logging

LOG = logging.getLogger(__name__)

# Order is important because we will retrieve by
# trying to find by name in substring and so PendingDeprecationWarning
# and DeprecationWarning could collid
BASE_DEPRECATIONS = [
    PendingDeprecationWarning,
    DeprecationWarning,
    FutureWarning,
]


class AnalyzerException(Exception):
    """Exceptions related to the module analyzer."""

    pass


class AnalyzerSyntaxException(Exception):
    """Exceptions related to the module analyzer."""

    pass


def find_exceptions_recursively(root, results=None, previous=None):
    """Recursively walk through an AST tree to looking for all exceptions.

    Here we don't care about the type of the raised exception, we just
    want to get all of them.

    This function is recursive that mean that while a node have classes or
    functions inside of it, then they (child node) will be analyzed too.

    :param ast root: AST node to walk through.
    :param list results: List of results to append.
    :param ast previous: AST node previously analyzed.
    :return: List of results founds
    """
    if not results:
        results = []
    previous = root
    for node in ast.iter_child_nodes(root):
        # an Exception is raised? If yes then we add her to results.
        if isinstance(node, ast.Raise):
            results.append(
                {
                    "lineno": "{func}:{raised}".format(
                        func=previous.lineno, raised=node.lineno
                    ),
                    "def": previous,
                    "raise": node,
                }
            )
        # We just care about the exceptions raised in module, classes
        # or functions. In other words ignore other kinds of nodes.
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
            results = find_exceptions_recursively(node, results)
    return results


def get_node_source(source, node):
    """Retrieve the original source code (human readable) of a node.

    :param list source: List of line of source code.
    :param ast node: AST node to retrieve in source code list.
    """
    return ast.get_source_segment(source, node)


def retrieve_code(results, content):
    """Retrieve original code of the AST detected as raising exception.

    When raised exceptions are detected in the AST then we put the
    corresponding line number in results and this function aim to retrieve
    the original code of the parsed AST to tokenize to extract needed
    infos.

    :return: lines of source code that corresponding to the AST tree.
    """
    source_lines = []
    for el in results:
        raise_line = get_node_source(content, el["raise"])
        for depr in BASE_DEPRECATIONS:
            if depr.__name__ not in raise_line:
                continue
            def_line = get_node_source(content, el["def"])
            source_lines.append({"def": def_line, "raise": raise_line})
            break
    return source_lines


def tokenizer(snippet):
    """Tokenize the given snippet of source code.

    :param string snippet: Source code to tokenize.

    :return: list of tokens
    """
    if not isinstance(snippet, io.BytesIO):
        snippet = io.BytesIO(snippet.encode("utf-8"))
    return [el for el in tokenize.tokenize(snippet.readline)]


def extract_function_name(tokens):
    """Retrieve function name from the given token list.

    Given tokens should correspond to the isolated source code of
    the catched function.

    :param string tokens: tokens to parse.

    :return: the function name at string format.
    """
    name = None
    ignored = ["def"]
    for token in tokens:
        if int(token.type) == NEEDED_TOKENS_TYPES["OP"]:
            break
        if int(token.type) == NEEDED_TOKENS_TYPES["ENCODING"]:
            continue
        if token.string in ignored:
            continue
        name = token.string
    return name


def extract_exception_type(tokens):
    """Retrieve the exception type from the given token list.

    Given tokens should correspond to the isolated source code of
    the catched exception.

    :param string tokens: tokens to parse.

    :return: the function name at string format.
    """
    name = None
    ignored = ["def"]
    for token in tokens:
        if int(token.type) == NEEDED_TOKENS_TYPES["OP"]:
            return name
        if int(token.type) == NEEDED_TOKENS_TYPES["ENCODING"]:
            continue
        if token.string in ignored:
            continue
        name = token.string


# We don't need to list all tokens types only few of them
# are useful here
NEEDED_TOKENS_TYPES = {
    "ENCODING": 62,
    "NAME": 1,
    "OP": 54,
    "NEWLINE": 4,
    "INDENT": 5,
}


class ModuleAnalyzer:
    def __init__(self, module_path, custome_deprecations=None):
        """Analyzer that aim to detect deprecations.

        This class allow you to analyze a specified module to
        detect if it contains deprecated things.

        If a deprecation warning is raised somewhere in a function this
        function will be consider as deprecated and will be added to results.

        Are considered as deprecated functions where one of the following
        exceptions are raised:
        - DeprecationWarning
        - FutureWarning
        - PendingDeprecationWarning

        To retrieve this information this class will analyze the AST syntax
        of the module to retrieve all functions/classes where the previous
        exceptions are raised.

        When deprecations are found in a module this analyzer will
        tokenize its code to retrieve the called function name wherein the
        deprecation is raised.

        You can pass custome deprecations to looking for by example if
        you want to also detect the debtcollector's deprecations exceptions.

        :param string module_path: Path of module to analyze.
        :param list custome_deprecations: List of custome deprecation types
                                          to looking for.
        :return: Return a list of results (function name, exceptions type).
        """
        # Allow to pass Path and string as module_path
        if isinstance(module_path, Path):
            self.module_path = str(module_path)
        else:
            self.module_path = module_path
        self.ast = None
        self.code = None
        self.tokens = None
        self.results = []
        self.content = None
        if custome_deprecations and isinstance(custome_deprecations, list):
            global BASE_DEPRECATIONS
            BASE_DEPRECATIONS.extends(custome_deprecations)
        try:
            with open(module_path, "r", errors="ignore") as fp:
                self.content = fp.read()
        # Handle file handling errors (rights, unexisting files, etc...)
        except (OSError, IOError) as err:
            raise AnalyzerException(
                "Error detected during module opening ({})".format(str(err))
            )
        self.code = io.BytesIO(self.content.encode("utf-8"))
        try:
            self.ast = ast.parse(self.content)
        except SyntaxError as err:
            raise AnalyzerSyntaxException(str(err))
        self.tokens = [el for el in tokenize.tokenize(self.code.readline)]
        self.exceptions_found = find_exceptions_recursively(self.ast)

    def analyze(self):
        results = find_exceptions_recursively(self.ast)
        results = retrieve_code(results, self.content)
        for el in results:
            tokens_def = tokenizer(el["def"])
            tokens_raise = tokenizer(el["raise"])
            function_name = extract_function_name(tokens_def)
            exception_type = extract_exception_type(tokens_raise)
            self.results.append(
                {"func": function_name, "except": exception_type}
            )

import ast
import io
import tokenize
import unittest

from wardoff.analyzers import syntax as syntax_analyzer
from wardoff.tests import utils as tutils


class TestAnalyzerIsFunctions(unittest.TestCase):
    def setUp(self):
        self.module = str(tutils.TEST_BASE_DIR.joinpath("sample.py"))
        with open(self.module, "r") as fp:
            self.content = fp.read()
        self.code = io.BytesIO(self.content.encode("utf-8"))
        self.ast = ast.parse(self.content)
        self.tokens = [el for el in tokenize.tokenize(self.code.readline)]

    def test_find_exceptions_recursively(self):
        results = syntax_analyzer.find_exceptions_recursively(self.ast)
        self.assertTrue((results is not None))
        self.assertEqual(len(results), 6)

    def test_retrieve_code(self):
        results = syntax_analyzer.find_exceptions_recursively(self.ast)
        results = syntax_analyzer.retrieve_code(results, self.content)
        self.assertEqual(len(results), 5)
        self.assertEqual(results[0]["def"].split("\n")[0], "def fiz():")

    def test_tokenizer(self):
        results = syntax_analyzer.find_exceptions_recursively(self.ast)
        results = syntax_analyzer.retrieve_code(results, self.content)
        tokens = syntax_analyzer.tokenizer(results[0]["def"])
        self.assertTrue((tokens is not None))
        self.assertEqual(tokens[2].string, "fiz")
        tokens = syntax_analyzer.tokenizer(results[0]["raise"])
        self.assertTrue((tokens is not None))
        self.assertEqual(tokens[2].string, "DeprecationWarning")

    def test_extract_function_name(self):
        results = syntax_analyzer.find_exceptions_recursively(self.ast)
        results = syntax_analyzer.retrieve_code(results, self.content)
        tokens = syntax_analyzer.tokenizer(results[0]["def"])
        name = syntax_analyzer.extract_function_name(tokens)
        self.assertEqual(name, "fiz")


class TestModuleAnalyzer(unittest.TestCase):
    def setUp(self):
        self.module = tutils.TEST_BASE_DIR.joinpath("sample.py")
        with open(str(self.module), "r") as fp:
            self.content = fp.read()
        self.code = io.BytesIO(self.content.encode("utf-8"))
        self.ast = ast.parse(self.content)
        self.tokens = [el for el in tokenize.tokenize(self.code.readline)]

    def test_init(self):
        self.module_analyzer = syntax_analyzer.ModuleAnalyzer(str(self.module))
        self.assertTrue((self.module_analyzer.tokens is not None))
        self.assertEqual(self.module_analyzer.tokens, self.tokens)
        self.assertTrue((self.module_analyzer.code is not None))
        self.assertTrue((self.module_analyzer.content is not None))
        self.assertTrue((self.module_analyzer.ast is not None))

    def test_init_with_path(self):
        self.module_analyzer = syntax_analyzer.ModuleAnalyzer(self.module)
        self.assertTrue((self.module_analyzer.tokens is not None))
        self.assertEqual(self.module_analyzer.tokens, self.tokens)
        self.assertTrue((self.module_analyzer.code is not None))
        self.assertTrue((self.module_analyzer.content is not None))
        self.assertTrue((self.module_analyzer.ast is not None))

    def test_failing_init(self):
        with self.assertRaises(syntax_analyzer.AnalyzerException) as err:
            self.module_analyzer = syntax_analyzer.ModuleAnalyzer("/bim/boom")
            self.assertEqual(
                err,
                "Error detected during module opening "
                "([Errno 2] No such file or directory: "
                "'/bim/boom')",
            )

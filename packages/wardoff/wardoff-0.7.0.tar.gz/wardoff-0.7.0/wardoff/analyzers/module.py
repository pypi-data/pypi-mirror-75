from pathlib import Path

from wardoff import logging, utils, venv
from wardoff.analyzers import syntax
from wardoff.package import Package

LOG = logging.getLogger(__name__)


class ModuleAnalyzerInitializationError(Exception):
    pass


class BaseAnalyzer:
    def __init__(self, project):
        """Project requirements analyzer.

        Base analyzer class.

        :param string project: Project to analyze.
        """
        self.project = project
        self.ignore_extra_req = False
        self.dont_reinstall = False
        self.requirements = []

    def analyze(self):
        self.retrieve_requirements()
        self.search_deprecated()

    def set_ignore_extra_req(self, ignore):
        self.ignore_extra_req = ignore

    def set_dont_reinstall(self, dont_reinstall):
        self.dont_reinstall = dont_reinstall

    def retrieve_requirements(self):
        raise NotImplementedError("retrieve method not implemented")

    def get_results(self):
        return self.results

    def get_stats(self):
        stats = {
            "nb_analyzed_mod": len(self.requirements),
        }
        LOG.debug(stats)
        return stats

    def search_deprecated(self):
        self.results = []
        for el in self.requirements:
            LOG.debug(el)
            if not el.sources_path:
                continue
            deprecations = []
            for pyfile in utils.get_pyfiles(el.sources_path):
                try:
                    mod_analyzer = syntax.ModuleAnalyzer(pyfile)
                except syntax.AnalyzerSyntaxException:
                    continue
                mod_analyzer.analyze()
                if mod_analyzer.results:
                    res = {"module": pyfile, "results": mod_analyzer.results}
                    deprecations.extends(res)
            if not deprecations:
                continue
            self.results.append({"pkg": el, "deprecations": deprecations})
            LOG.debug(deprecations)


class PathAnalyzer(BaseAnalyzer):
    def retrieve_requirements(self):
        if self.dont_reinstall:
            LOG.info("Skipping requirements installation")
        else:
            path = Path(self.project)
            # let's suppose that requirements file will be caught by the
            # following rules so we can say that is some sort of best practice
            # for a python project to define it's requirements in a
            # requirements.txt files.
            requirements_files = list(path.glob("**/*requirements.txt"))
            requirements_files.extend(list(path.glob("**/*requirements*.txt")))
            requirements_files.extend(list(path.glob("**/requirements*.txt")))
            requirements_files.extend(list(path.glob("requirements*.txt")))
            if path.joinpath("requirements.txt").is_file():
                requirements_files.append(path.joinpath("requirements.txt"))
            if path.joinpath("doc", "requirements.txt").is_file():
                requirements_files.append(
                    path.joinpath("doc", "requirements.txt")
                )
            for reqf in requirements_files:
                # we choose to ignore all sort of virtualenv in the contained
                # in the current path based on the dot prefix of `p`
                if str(reqf).startswith("."):
                    continue
                if (
                    "doc" in str(reqf) or "test" in str(reqf)
                ) and self.ignore_extra_req:
                    continue
                venv.pip_install("-r", str(reqf))

        self.requirements = [Package(el) for el in venv.pip_freeze()]


class FileAnalyzer(BaseAnalyzer):
    pass


class RepoAnalyzer(BaseAnalyzer):
    pass


class PackageAnalyzer(BaseAnalyzer):
    def retrieve_requirements(self):
        if not self.dont_reinstall:
            venv.pip_install(self.project)
        self.requirements = [
            Package(el) for el in venv.pip_freeze([self.project])
        ]
        LOG.debug(self.requirements)

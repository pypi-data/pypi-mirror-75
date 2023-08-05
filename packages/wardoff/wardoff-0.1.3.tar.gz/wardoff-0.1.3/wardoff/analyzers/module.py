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

    def analyze(self):
        self.requirements = self.retrieve_requirements()

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


class PathAnalyzer(BaseAnalyzer):
    def retrieve_requirements(self):
        requirements = []
        path = Path(self.project)
        requirements_files = list(path.glob("**/*requirements.txt"))
        for p in requirements_files:
            with p.open() as f:
                requirements.extend(f.readlines())
        return requirements


class FileAnalyzer(BaseAnalyzer):
    pass


class RepoAnalyzer(BaseAnalyzer):
    pass


class PackageAnalyzer(BaseAnalyzer):
    def __init__(self, project):
        """Analyze a module installed from pypi.

        :param string project: Project to analyze.
        """
        self.project = project
        venv.create()

    def analyze(self):
        self.retrieve_requirements()
        self.search_deprecated()

    def retrieve_requirements(self):
        venv.pip_install(self.project)
        self.requirements = [
            Package(el) for el in venv.pip_freeze([self.project])
        ]
        LOG.debug(self.requirements)

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

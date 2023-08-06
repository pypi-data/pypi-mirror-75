from pathlib import Path

from wardoff import venv


class PackageError(Exception):
    pass


class Package:
    def __init__(self, pkg):
        """Abstraction module to represent the given package.

        This class aim to represent the given package and to provide some
        shortcut to retrieve related infos like the package module path,
        it's name, it's version, etc.

        :param str pkg: Package name to handle
        """
        self.metadata = []
        try:
            self.name, self.version = pkg.split("==")
        except ValueError:
            raise PackageError("package version not found ({})".format(pkg))
        self.retrieve_infos()

    def retrieve_infos(self):
        self.sources_path = None
        for el in venv.pip_show(self.name):
            # we will assign attribut to this
            # living object by retrieving key value by spliting on
            # colon (:), however url(http://) can be present in value and
            # it can collid with your detection so let's replace url
            # schema by a dedicated keyword to avoid this situation
            # and ensure us to can unconvert to the original url.
            if "http" in el:
                el = el.replace("https:", "$$secure_url$$")
                el = el.replace("http:", "$$url$$")
            # we want key to lowercase to standardize syntax
            key = el.lower().split(":")[0].strip()
            try:
                value = el.split(":")[1].strip()
            except IndexError:
                value = ""
            setattr(self, key, value)
        if getattr(self, "location"):
            top_level = Path(self.location).joinpath(
                "{name}-{version}.dist-info".format(
                    name=self.name, version=self.version
                ),
                "top_level.txt",
            )
            if top_level.is_file():
                with open(str(top_level)) as fp:
                    levels = fp.readlines()
                for level in levels:
                    plevel = Path(self.location).joinpath(
                        level.replace("\n", "")
                    )
                    if plevel.is_dir() or plevel.is_file():
                        self.sources_path = plevel

            metadata = Path(self.location).joinpath(
                "{name}-{version}.dist-info".format(
                    name=self.name, version=self.version
                ),
                "METADATA",
            )
            if metadata.is_file():
                with open(str(metadata)) as fp:
                    for line in fp.readlines():
                        if not line.startswith("Classifier:"):
                            continue
                        classifier = (
                            line.replace("Classifier:", "")
                            .replace("\n", "")
                            .strip()
                        )
                        self.metadata.append(classifier)

    def supported_python_versions(self):
        versions = []
        for metadata in self.metadata:
            if metadata.startswith("Programming Language :: Python ::"):
                version = metadata.split("::")[2].strip()
                if version == "Implementation":
                    continue
                versions.append(version)
        return versions

    def module_is_single_file(self):
        return Path(self.location).joinpath(self.name).is_file()

    def module_is_dir(self):
        return Path(self.location).joinpath(self.name).is_dir()

    def __str__(self):
        """Get the string representation of the given module.

        Package objects are represented by "name==version".
        """
        return "{}=={}".format(self.name, self.version)

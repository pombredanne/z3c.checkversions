from pkg_resources import parse_version, Requirement
from setuptools import package_index

class Checker(object):
    """Base class for version checkers
    """
    __custom_url = False
    def __init__(self, filename=None, index_url=None):
        self.filename = filename
        self.pi = package_index.PackageIndex()
        self._set_index_url(index_url)
        if index_url is not None:
            self.__custom_url = True

    def _set_index_url(self, url):
        """set the index URL
        """
        if url is not None:
            self.pi.index_url = url
        if not self.pi.index_url.endswith('/'):
            self.pi.index_url += '/'

    def check(self, level=0):
        """Search new versions in a version list
        versions must be a dict {'name': 'version'}

        The new version is limited to the given level:
        Example with version x.y.z
        level = 0: checks new version x
        level = 1: checks new version y
        level = 2: checks new version z

        By default, the highest version is found.
        """
        versions = self.get_versions()

        for name, version in versions.items():
            parsed_version = parse_version(version)
            req = Requirement.parse(name)
            self.pi.find_packages(req)
            new_dist = None
            # loop all versions until we find the first newer version
            # that keeps the major versions (below level)
            for dist in self.pi[req.key]:
                if dist.parsed_version[:level] > parsed_version[:level]:
                    continue
                new_dist = dist
                break


            if new_dist and new_dist.parsed_version > parsed_version:
                print("%s=%s" % (name, new_dist.version))


    def get_versions(self):
        raise NotImplementedError
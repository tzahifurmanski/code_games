import logging
from collections import defaultdict
log = logging.getLogger(__name__)


class DependenciesCache:
    # TODO: Add expiration to the 'latest' entries in the cache
    #  (only latest, since I assume already released versions does not update their dependencies)
    #  or add a batch job to update the cache periodically so it'll always be up to date
    # TODO: Add persistency to the cache

    def __init__(self, packages_info_client):
        self.cache = defaultdict(dict)
        self.packages_info_client = packages_info_client

    def get(self, name, version):
        # If package info is in cache, return it
        if name in self.cache and version in self.cache[name]:
            log.debug("Cache hit - Package {}-{} was found in cache.".format(name, version))
            return self.cache[name][version]

        # Otherwise, get the package info from the package info client and return it
        log.debug("Cache miss - Retrieving package {}-{} dependencies from npm.".format(name, version))

        package_info = self.packages_info_client.get_package_information(name, version)
        dependencies = package_info.get('dependencies', dict())
        self.cache[name][version] = dependencies

        # If version is latest, save the resolved dependencies also with the actual version
        if version == 'latest':
            updated_version = package_info.get('version', version)
            self.cache[name][updated_version] = dependencies

        return dependencies

from queue import Queue
import logging

log = logging.getLogger(__name__)


class DependencyMapper:
    SUMMARY_LOG_MESSAGE = "Dependencies tree for package {name}-{version} retrieved.{count} dependencies were found."

    def __init__(self, cache):
        self.cache = cache

    @staticmethod
    def _create_package_dict(name, version):
        return {
            'name': name,
            'version': version
        }

    @staticmethod
    def _get_explicit_version(package_version):
        # TODO: Better handle semantic versioning and conditions - ^, ~, ||.
        #  and things like:
        #  {
        #       "name": "safer-buffer",
        #       "version": ">= 2.1.2 < 3"
        #  }
        #  For now I'm only extracting the first version number I find
        version = package_version.replace('~', '').replace('^', '')
        return version.strip('><= .|&').split(' ')[0]

    def get_dependencies_tree_for_package(self, name, version):
        log.debug("Retrieving dependencies tree for package {}-{}...".format(name, version))

        dependencies_queue = Queue()
        total_num_of_dependencies = 0
        root_package = self._create_package_dict(name, version)
        dependencies_queue.put(root_package)

        while not dependencies_queue.empty():
            package = dependencies_queue.get()
            package_dependencies = self.cache.get(package['name'], package['version'])

            sub_dependencies = list()

            for dep_name, dep_version in package_dependencies.items():
                dep_version = self._get_explicit_version(dep_version)

                child = self._create_package_dict(dep_name, dep_version)
                dependencies_queue.put(child)
                sub_dependencies.append(child)

            # If the package has dependencies, add them to the package object
            if sub_dependencies:
                package['dependencies'] = sub_dependencies
                total_num_of_dependencies += len(sub_dependencies)

        log.debug(self.SUMMARY_LOG_MESSAGE.format(name=name, version=version, count=total_num_of_dependencies))

        # Return just the dependencies, or an empty list
        return root_package.get('dependencies', list())

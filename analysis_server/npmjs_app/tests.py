import pytest
from django.test import Client
from django.urls import reverse
from http import HTTPStatus

from dependency_resolving.dependencies_cache import DependenciesCache


@pytest.fixture
def client():
    return Client()


class PackageInfoServiceForTest:
    def __init__(self, dependencies=None):
        self.results_dependencies = dependencies

    def get_package_information(self, name, version):
        package = {
            "name": name,
            "version": version
        }
        if self.results_dependencies:
            package['dependencies'] = self.results_dependencies

        return package


class TestDependenciesCache:
    # In a more complex flow I'd add mocking to the logger so it'd be easier to track the flow
    def test_requesting_an_entry_already_in_cache(self):
        # Given - A cache with one entry
        package_name = "Zigi"
        package_version = "1.0"
        package_dependencies = [
            {
                'name': 'one',
                'version': '2.0'
            }
        ]
        cache = DependenciesCache(PackageInfoServiceForTest)
        cache.cache[package_name][package_version] = package_dependencies

        # When - Asking for an entry that's already in the cache
        dependencies = cache.get(package_name, package_version)

        # Then - The entry is found, no resolving is done and dependencies are returned
        assert package_dependencies == dependencies

    def test_requesting_a_new_entry(self):
        # Given - A cache with no entries
        mocked_dependencies = [{
            'name': 'zigi_son',
            'version': '2.0'
        }]
        cache = DependenciesCache(PackageInfoServiceForTest(mocked_dependencies))

        # When - Asking for an entry not in cache
        package_name = "Zigi"
        package_version = "1.0"

        dependencies = cache.get(package_name, package_version)

        # Then - The entry is resolved and mocked dependencies are returned
        assert mocked_dependencies == dependencies


# TODO: This can be split to UT and integration tests and then mocking for NPMJS can be added for UT
class TestDependencyTreeView:
    # Usually I'd separate the view tests and the DependencyMapper tests but
    # in this case the view is lean enough for joined tests
    def test_no_package_name_supplied(self, client):
        # When - Requesting dependencies details without specifying a package
        result = client.get(reverse('dependency-tree', kwargs={'name': ''}))

        # Then - A bad request error is returned
        assert result.status_code == HTTPStatus.BAD_REQUEST
        assert result.data[0] == "Missing package name"

    def test_package_not_found(self, client):
        # Given - A name of a package that does not exist
        package_name = 'Zigi-Package'

        # When - Requesting dependencies details about a package that does not exist
        result = client.get(reverse('dependency-tree', kwargs={'name': package_name}))

        # Then - An empty response is returned
        assert result.status_code == HTTPStatus.NOT_FOUND
        assert result.data == "Package {} was not found".format(package_name)

    def test_package_with_no_dependencies(self, client):
        # Given - A package that has no dependencies
        package_name = 'mime-db'

        # When - Requesting dependencies details of the package
        result = client.get(reverse('dependency-tree', kwargs={'name': package_name}))

        # Then - An empty list is returned
        assert result.status_code == HTTPStatus.OK
        assert result.data == []

    def test_package_with_one_level_of_dependencies(self, client):
        # Given - A package that has one level of dependencies
        package_name = 'mime-types'

        # When - Requesting dependencies details of the package
        result = client.get(reverse('dependency-tree', kwargs={'name': package_name}))

        # Then - A bad request error is returned
        assert result.status_code == HTTPStatus.OK
        assert result.data == [
            {
                'name': 'mime-db',
                'version': '1.42.0'
            }
        ]

    def test_package_with_multiple_levels(self, client):
        # Given - A package that has multiple levels of dependencies
        package_name = 'accepts'

        # When - Requesting dependencies details of the package
        result = client.get(reverse('dependency-tree', kwargs={'name': package_name}))

        # Then - A bad request error is returned
        assert result.status_code == HTTPStatus.OK
        assert result.data == [
            {
                'name': 'mime-types',
                'version': '2.1.24',
                'dependencies': [
                    {
                        'name': 'mime-db',
                        'version': '1.40.0'
                    }
                ]
            },
            {
                'name': 'negotiator',
                'version': '0.6.2'
            }
        ]

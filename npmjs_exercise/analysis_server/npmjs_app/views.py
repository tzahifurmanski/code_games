from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from http import HTTPStatus

from npmjs_app.dependency_resolving.dependencies_cache import DependenciesCache
from npmjs_app.dependency_resolving.dependency_mapper import DependencyMapper
from npmjs_app.dependency_resolving.npmjs_client import NPMJSClient, PackageNotFound


class DependencyTreeView(APIView):
    # Thought about saving the whole sub tree so we can save on getting info for
    #  every sub package and go for cache for whole dependency trees,
    #  but I don't think it'll save much
    cache = DependenciesCache(NPMJSClient)
    mapper = DependencyMapper(cache)

    # If packages resolving takes too much time, we can add the ability to query asynchronously -
    #  in this case, return an id for a query request, and an api to get the request status/results.
    # noinspection PyUnusedLocal
    def get(self, request, name, version):
        if not name:
            raise ValidationError("Missing package name")
        if not version:
            raise ValidationError("Missing package version")

        try:
            # I assume latest since exercise did not specify sending a version
            result = self.mapper.get_dependencies_tree_for_package(name, version)
            if not result:
                return Response(status=HTTPStatus.NOT_FOUND,
                                data="Not dependencies were found for package {} and version {}".format(name, version))

        except PackageNotFound:
            return Response(status=HTTPStatus.NOT_FOUND, data="Package {} with version {}, was not found".format(name, version))

        return Response(result)


dependency_tree_view = DependencyTreeView.as_view()

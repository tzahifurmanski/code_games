import requests
import json
import logging

log = logging.getLogger(__name__)


# TODO: Add metrics


class PackageNotFound(Exception):
    pass


class NPMJSClient:
    PACKAGE_INFO_URL = "https://registry.npmjs.org/{package_name}/{package_version}"

    @classmethod
    def get_package_information(cls, name, version):
        log.debug("Querying NPMJS for information on package {}-{}...".format(name, version))
        response = requests.Session().get(cls.PACKAGE_INFO_URL.format(package_name=name, package_version=version))
        response_text = json.loads(response.text)
        # TODO: I assume that only root packages can be missing. If not, need to handle that
        # TODO: Need to handle a scenario where a the package exist but a specific version is not found
        #  and 'version not found' is returned
        if response_text == 'Not Found':
            raise PackageNotFound()

        log.debug("Done querying NPMJS for information on package {}-{}.".format(name, version))

        return response_text

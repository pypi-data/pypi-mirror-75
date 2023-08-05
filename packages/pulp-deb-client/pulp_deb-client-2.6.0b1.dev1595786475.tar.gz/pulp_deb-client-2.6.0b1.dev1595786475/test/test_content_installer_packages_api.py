# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import pulpcore.client.pulp_deb
from pulpcore.client.pulp_deb.api.content_installer_packages_api import ContentInstallerPackagesApi  # noqa: E501
from pulpcore.client.pulp_deb.rest import ApiException


class TestContentInstallerPackagesApi(unittest.TestCase):
    """ContentInstallerPackagesApi unit test stubs"""

    def setUp(self):
        self.api = pulpcore.client.pulp_deb.api.content_installer_packages_api.ContentInstallerPackagesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create(self):
        """Test case for create

        """
        pass

    def test_list(self):
        """Test case for list

        """
        pass

    def test_read(self):
        """Test case for read

        """
        pass


if __name__ == '__main__':
    unittest.main()

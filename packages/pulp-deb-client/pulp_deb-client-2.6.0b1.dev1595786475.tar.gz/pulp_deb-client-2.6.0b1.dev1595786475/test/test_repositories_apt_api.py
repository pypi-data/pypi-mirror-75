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
from pulpcore.client.pulp_deb.api.repositories_apt_api import RepositoriesAptApi  # noqa: E501
from pulpcore.client.pulp_deb.rest import ApiException


class TestRepositoriesAptApi(unittest.TestCase):
    """RepositoriesAptApi unit test stubs"""

    def setUp(self):
        self.api = pulpcore.client.pulp_deb.api.repositories_apt_api.RepositoriesAptApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create(self):
        """Test case for create

        """
        pass

    def test_delete(self):
        """Test case for delete

        """
        pass

    def test_list(self):
        """Test case for list

        """
        pass

    def test_modify(self):
        """Test case for modify

        Modify Repository Content  # noqa: E501
        """
        pass

    def test_partial_update(self):
        """Test case for partial_update

        """
        pass

    def test_read(self):
        """Test case for read

        """
        pass

    def test_sync(self):
        """Test case for sync

        Sync from remote  # noqa: E501
        """
        pass

    def test_update(self):
        """Test case for update

        """
        pass


if __name__ == '__main__':
    unittest.main()

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

import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.api.content_modulemds_api import ContentModulemdsApi  # noqa: E501
from pulpcore.client.pulp_rpm.rest import ApiException


class TestContentModulemdsApi(unittest.TestCase):
    """ContentModulemdsApi unit test stubs"""

    def setUp(self):
        self.api = pulpcore.client.pulp_rpm.api.content_modulemds_api.ContentModulemdsApi()  # noqa: E501

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

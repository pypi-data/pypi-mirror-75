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

import pulpcore.client.pulp_ansible
from pulpcore.client.pulp_ansible.api.pulp_ansible_tags_api import PulpAnsibleTagsApi  # noqa: E501
from pulpcore.client.pulp_ansible.rest import ApiException


class TestPulpAnsibleTagsApi(unittest.TestCase):
    """PulpAnsibleTagsApi unit test stubs"""

    def setUp(self):
        self.api = pulpcore.client.pulp_ansible.api.pulp_ansible_tags_api.PulpAnsibleTagsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_list(self):
        """Test case for list

        """
        pass


if __name__ == '__main__':
    unittest.main()

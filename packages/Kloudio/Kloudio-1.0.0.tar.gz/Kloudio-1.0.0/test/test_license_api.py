# coding: utf-8

"""
    Kloudio APIs

"""


from __future__ import absolute_import

import unittest

import kloudio
from kloudio.api.license_api import LicenseApi  # noqa: E501
from kloudio.rest import ApiException


class TestLicenseApi(unittest.TestCase):
    """LicenseApi unit test stubs"""

    def setUp(self):
        self.api = kloudio.api.license_api.LicenseApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_license(self):
        """Test case for create_license

        Create a license  # noqa: E501
        """
        pass

    def test_delete_license(self):
        """Test case for delete_license

        Delete a license  # noqa: E501
        """
        pass

    def test_get_licenses(self):
        """Test case for get_licenses

        Get all licenses  # noqa: E501
        """
        pass

    def test_update_license(self):
        """Test case for update_license

        Update a license  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()

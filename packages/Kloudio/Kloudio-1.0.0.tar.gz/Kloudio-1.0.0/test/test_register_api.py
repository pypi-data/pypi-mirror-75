# coding: utf-8

"""
    Kloudio APIs

"""


from __future__ import absolute_import

import unittest

import kloudio
from kloudio.api.register_api import RegisterApi  # noqa: E501
from kloudio.rest import ApiException


class TestRegisterApi(unittest.TestCase):
    """RegisterApi unit test stubs"""

    def setUp(self):
        self.api = kloudio.api.register_api.RegisterApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_register_user(self):
        """Test case for register_user

        Register a user  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()

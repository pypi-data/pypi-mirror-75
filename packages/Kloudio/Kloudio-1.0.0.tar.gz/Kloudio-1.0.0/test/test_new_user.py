# coding: utf-8

"""
    Kloudio APIs

"""


from __future__ import absolute_import

import unittest
import datetime

import kloudio
from kloudio.models.new_user import NewUser  # noqa: E501
from kloudio.rest import ApiException

class TestNewUser(unittest.TestCase):
    """NewUser unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test NewUser
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = kloudio.models.new_user.NewUser()  # noqa: E501
        if include_optional :
            return NewUser(
                email = 'admin@kloud.io', 
                first_name = 'John', 
                password = 'myStrongPassword', 
                last_name = 'Doe'
            )
        else :
            return NewUser(
                email = 'admin@kloud.io',
                first_name = 'John',
                password = 'myStrongPassword',
        )

    def testNewUser(self):
        """Test NewUser"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

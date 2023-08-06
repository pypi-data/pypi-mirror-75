# coding: utf-8

"""
    Kloudio APIs

"""


from __future__ import absolute_import

import unittest
import datetime

import kloudio
from kloudio.models.update_connection import UpdateConnection  # noqa: E501
from kloudio.rest import ApiException

class TestUpdateConnection(unittest.TestCase):
    """UpdateConnection unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test UpdateConnection
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = kloudio.models.update_connection.UpdateConnection()  # noqa: E501
        if include_optional :
            return UpdateConnection(
                name = 'demo-connection', 
                host = 'localhost', 
                port = '1234', 
                database = 'users', 
                username = 'admin', 
                password = 'password', 
                production = True, 
                ssl = True, 
                enable_tunnel = True, 
                tunnel_info = None, 
                ssl_info = None
            )
        else :
            return UpdateConnection(
        )

    def testUpdateConnection(self):
        """Test UpdateConnection"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

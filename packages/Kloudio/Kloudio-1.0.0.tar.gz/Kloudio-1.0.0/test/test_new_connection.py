# coding: utf-8

"""
    Kloudio APIs

"""


from __future__ import absolute_import

import unittest
import datetime

import kloudio
from kloudio.models.new_connection import NewConnection  # noqa: E501
from kloudio.rest import ApiException

class TestNewConnection(unittest.TestCase):
    """NewConnection unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test NewConnection
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = kloudio.models.new_connection.NewConnection()  # noqa: E501
        if include_optional :
            return NewConnection(
                name = 'demo-connection', 
                host = 'localhost', 
                port = '1234', 
                database = 'users', 
                username = 'admin', 
                password = 'password', 
                connection_type = 'DATABASE', 
                db_type = 'MYSQL', 
                production = True, 
                ssl = True, 
                share_with = [], 
                enable_tunnel = True, 
                tunnel_info = None, 
                other_options = None, 
                fed = True, 
                dw = True, 
                metadata = '0', 
                integration_user_id = 1.337, 
                web_type = '0', 
                ssl_info = None
            )
        else :
            return NewConnection(
                name = 'demo-connection',
                host = 'localhost',
                port = '1234',
                database = 'users',
                username = 'admin',
                password = 'password',
                connection_type = 'DATABASE',
                db_type = 'MYSQL',
        )

    def testNewConnection(self):
        """Test NewConnection"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

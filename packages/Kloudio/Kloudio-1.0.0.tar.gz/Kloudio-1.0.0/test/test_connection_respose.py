# coding: utf-8

"""
    Kloudio APIs

"""


from __future__ import absolute_import

import unittest
import datetime

import kloudio
from kloudio.models.connection_respose import ConnectionRespose  # noqa: E501
from kloudio.rest import ApiException

class TestConnectionRespose(unittest.TestCase):
    """ConnectionRespose unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ConnectionRespose
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = kloudio.models.connection_respose.ConnectionRespose()  # noqa: E501
        if include_optional :
            return ConnectionRespose(
                id = '0', 
                name = '0', 
                host = '0', 
                port = '0', 
                database = '0', 
                username = '0', 
                password = '0', 
                db_type = '0', 
                production = True, 
                user = 1.337, 
                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                ssl = True, 
                updated_by = '0', 
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                shared_with = None, 
                enable_tunnel = True, 
                tunnel_info = None, 
                other_options = None, 
                fed = True, 
                dw = True, 
                metadata = '0', 
                connection_type = '0', 
                integration_user_id = 1.337, 
                web_type = '0', 
                ssl_info = None
            )
        else :
            return ConnectionRespose(
                id = '0',
                name = '0',
                host = '0',
                port = '0',
                database = '0',
        )

    def testConnectionRespose(self):
        """Test ConnectionRespose"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

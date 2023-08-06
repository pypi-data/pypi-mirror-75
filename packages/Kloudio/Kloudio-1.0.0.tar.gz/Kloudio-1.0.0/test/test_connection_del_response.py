# coding: utf-8

"""
    Kloudio APIs

"""


from __future__ import absolute_import

import unittest
import datetime

import kloudio
from kloudio.models.connection_del_response import ConnectionDelResponse  # noqa: E501
from kloudio.rest import ApiException

class TestConnectionDelResponse(unittest.TestCase):
    """ConnectionDelResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ConnectionDelResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = kloudio.models.connection_del_response.ConnectionDelResponse()  # noqa: E501
        if include_optional :
            return ConnectionDelResponse(
                object = 'connection', 
                id = 'hwuhuwE&WYE12weA31', 
                deleted = True
            )
        else :
            return ConnectionDelResponse(
                object = 'connection',
                id = 'hwuhuwE&WYE12weA31',
                deleted = True,
        )

    def testConnectionDelResponse(self):
        """Test ConnectionDelResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

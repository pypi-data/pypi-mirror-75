# coding: utf-8

"""
    Kloudio APIs

"""


from __future__ import absolute_import

import unittest
import datetime

import kloudio
from kloudio.models.report_del_response import ReportDelResponse  # noqa: E501
from kloudio.rest import ApiException

class TestReportDelResponse(unittest.TestCase):
    """ReportDelResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ReportDelResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = kloudio.models.report_del_response.ReportDelResponse()  # noqa: E501
        if include_optional :
            return ReportDelResponse(
                object = 'report', 
                id = 'hwuhuwE&WYE12weA31', 
                deleted = True
            )
        else :
            return ReportDelResponse(
                object = 'report',
                id = 'hwuhuwE&WYE12weA31',
                deleted = True,
        )

    def testReportDelResponse(self):
        """Test ReportDelResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

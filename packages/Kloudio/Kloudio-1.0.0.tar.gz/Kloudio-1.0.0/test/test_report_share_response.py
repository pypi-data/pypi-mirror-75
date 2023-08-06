# coding: utf-8

"""
    Kloudio APIs

"""


from __future__ import absolute_import

import unittest
import datetime

import kloudio
from kloudio.models.report_share_response import ReportShareResponse  # noqa: E501
from kloudio.rest import ApiException

class TestReportShareResponse(unittest.TestCase):
    """ReportShareResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ReportShareResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = kloudio.models.report_share_response.ReportShareResponse()  # noqa: E501
        if include_optional :
            return ReportShareResponse(
                id = 'asd5AGWq-a@3', 
                object = 'report', 
                shared_with = [{"id":87,"email":"satish@kloud.io","access":"Can Edit","inviterEmail":"lgkd333@kloud.io"}]
            )
        else :
            return ReportShareResponse(
                id = 'asd5AGWq-a@3',
                object = 'report',
                shared_with = [{"id":87,"email":"satish@kloud.io","access":"Can Edit","inviterEmail":"lgkd333@kloud.io"}],
        )

    def testReportShareResponse(self):
        """Test ReportShareResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

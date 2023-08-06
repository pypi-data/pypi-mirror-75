# coding: utf-8

"""
    Kloudio APIs

"""


from __future__ import absolute_import

import unittest
import datetime

import kloudio
from kloudio.models.share_report import ShareReport  # noqa: E501
from kloudio.rest import ApiException

class TestShareReport(unittest.TestCase):
    """ShareReport unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ShareReport
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = kloudio.models.share_report.ShareReport()  # noqa: E501
        if include_optional :
            return ShareReport(
                id = 87, 
                email = '0', 
                access = '0'
            )
        else :
            return ShareReport(
                id = 87,
                email = '0',
                access = '0',
        )

    def testShareReport(self):
        """Test ShareReport"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

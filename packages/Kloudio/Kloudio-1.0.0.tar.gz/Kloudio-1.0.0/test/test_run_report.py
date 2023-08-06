# coding: utf-8

"""
    Kloudio APIs

"""


from __future__ import absolute_import

import unittest
import datetime

import kloudio
from kloudio.models.run_report import RunReport  # noqa: E501
from kloudio.rest import ApiException

class TestRunReport(unittest.TestCase):
    """RunReport unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test RunReport
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = kloudio.models.run_report.RunReport()  # noqa: E501
        if include_optional :
            return RunReport(
                _query_params = [], 
                preview_rows = 10
            )
        else :
            return RunReport(
        )

    def testRunReport(self):
        """Test RunReport"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

# coding: utf-8

"""
    Kloudio APIs

"""


from __future__ import absolute_import

import unittest
import datetime

import kloudio
from kloudio.models.new_job import NewJob  # noqa: E501
from kloudio.rest import ApiException

class TestNewJob(unittest.TestCase):
    """NewJob unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test NewJob
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = kloudio.models.new_job.NewJob()  # noqa: E501
        if include_optional :
            return NewJob(
                destination = 'email', 
                report_name = 'mysql-report', 
                report_id = '57d3273aed8c3e1e1c0d3746', 
                report_params = None, 
                frequency = 'Hourly', 
                am_pm = 'am', 
                hour = '01', 
                minute = '45', 
                day = 'Monday', 
                description = 'This is a sample query', 
                spreadsheet_id = '1-sl-_DtdBUmbi-FyJOwc2dXGd6xX0xZstX7UzlsU_EA', 
                sheet_id = '193832851', 
                sheet_name = 'Sales-v2', 
                timezone = 'PST', 
                select_cols = users, 
                tags = 'users', 
                email_on_success = True, 
                email_on_error = True, 
                metadata = None, 
                template_id = 'Y-z-jjFZ0H3u3maN', 
                template_name = 'Template2404a', 
                job_type = 'EMAIL'
            )
        else :
            return NewJob(
                destination = 'email',
                report_name = 'mysql-report',
                report_id = '57d3273aed8c3e1e1c0d3746',
                frequency = 'Hourly',
                am_pm = 'am',
                hour = '01',
                minute = '45',
                day = 'Monday',
        )

    def testNewJob(self):
        """Test NewJob"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

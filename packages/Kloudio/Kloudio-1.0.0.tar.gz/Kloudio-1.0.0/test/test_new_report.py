# coding: utf-8

"""
    Kloudio APIs

"""


from __future__ import absolute_import

import unittest
import datetime

import kloudio
from kloudio.models.new_report import NewReport  # noqa: E501
from kloudio.rest import ApiException

class TestNewReport(unittest.TestCase):
    """NewReport unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test NewReport
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = kloudio.models.new_report.NewReport()  # noqa: E501
        if include_optional :
            return NewReport(
                name = 'mysql-report', 
                connection_id = 'LPdqQW-Kri0ZfU1a', 
                description = 'This is a sample query', 
                db_query = 'SELECT * FROM users;', 
                db_table = 'users', 
                sql_mode = True, 
                connection_type = 'DB', 
                _query_params = [], 
                selected_cols = [], 
                available_cols = [], 
                shared_with = [], 
                db_schema = '0', 
                db_database = 'kloud', 
                joins = {}, 
                custom_join = '0', 
                additional_info = {}, 
                join_tables = [], 
                settings = {}, 
                model = {}
            )
        else :
            return NewReport(
                name = 'mysql-report',
                connection_id = 'LPdqQW-Kri0ZfU1a',
        )

    def testNewReport(self):
        """Test NewReport"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

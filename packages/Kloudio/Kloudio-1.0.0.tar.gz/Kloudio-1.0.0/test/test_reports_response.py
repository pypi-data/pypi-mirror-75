# coding: utf-8

"""
    Kloudio APIs

"""


from __future__ import absolute_import

import unittest
import datetime

import kloudio
from kloudio.models.reports_response import ReportsResponse  # noqa: E501
from kloudio.rest import ApiException

class TestReportsResponse(unittest.TestCase):
    """ReportsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ReportsResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = kloudio.models.reports_response.ReportsResponse()  # noqa: E501
        if include_optional :
            return ReportsResponse(
                name = 'mysql-report', 
                id = 'LPdqQW-Kri0ZfU1a', 
                connection_id = 'LPdqQW-Kri0ZfU1a', 
                description = 'This is a sample query', 
                db_query = 'SELECT * FROM users;', 
                db_table = 'users', 
                sql_mode = True, 
                connection_type = 'DB', 
                _query_params = {}, 
                selected_cols = {}, 
                available_cols = {}, 
                shared_with = {}, 
                db_schema = '0', 
                tags = finance, money, 
                db_database = 'kloud', 
                joins = {}, 
                custom_join = '0', 
                additional_info = {}, 
                join_tables = {}, 
                settings = {}, 
                model = {}, 
                user_id = 87, 
                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                query_version = 2, 
                db_type = 'CUSTOMAPI', 
                domain = 'test.com'
            )
        else :
            return ReportsResponse(
                name = 'mysql-report',
                id = 'LPdqQW-Kri0ZfU1a',
                connection_id = 'LPdqQW-Kri0ZfU1a',
        )

    def testReportsResponse(self):
        """Test ReportsResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

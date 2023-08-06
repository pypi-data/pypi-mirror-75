# coding: utf-8

"""
    Kloudio APIs

"""


from __future__ import absolute_import

import unittest

import kloudio
from kloudio.api.reports_api import ReportsApi  # noqa: E501
from kloudio.rest import ApiException


class TestReportsApi(unittest.TestCase):
    """ReportsApi unit test stubs"""

    def setUp(self):
        self.api = kloudio.api.reports_api.ReportsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_report(self):
        """Test case for create_report

        Create a report  # noqa: E501
        """
        pass

    def test_delete_report(self):
        """Test case for delete_report

        Delete a report  # noqa: E501
        """
        pass

    def test_execute_report(self):
        """Test case for execute_report

        Execute a report  # noqa: E501
        """
        pass

    def test_get_report(self):
        """Test case for get_report

        Get a report  # noqa: E501
        """
        pass

    def test_get_reports(self):
        """Test case for get_reports

        Get all report  # noqa: E501
        """
        pass

    def test_share_report(self):
        """Test case for share_report

        Share a report  # noqa: E501
        """
        pass

    def test_update_report(self):
        """Test case for update_report

        Update a report  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()

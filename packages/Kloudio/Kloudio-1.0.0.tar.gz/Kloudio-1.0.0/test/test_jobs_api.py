# coding: utf-8

"""
    Kloudio APIs

"""


from __future__ import absolute_import

import unittest

import kloudio
from kloudio.api.jobs_api import JobsApi  # noqa: E501
from kloudio.rest import ApiException


class TestJobsApi(unittest.TestCase):
    """JobsApi unit test stubs"""

    def setUp(self):
        self.api = kloudio.api.jobs_api.JobsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_job(self):
        """Test case for create_job

        Create a job  # noqa: E501
        """
        pass

    def test_delete_job(self):
        """Test case for delete_job

        Delete a job  # noqa: E501
        """
        pass

    def test_disable_job(self):
        """Test case for disable_job

        Disable a job  # noqa: E501
        """
        pass

    def test_enable_job(self):
        """Test case for enable_job

        Enable a job  # noqa: E501
        """
        pass

    def test_resume_jobs(self):
        """Test case for resume_jobs

        Resume jobs  # noqa: E501
        """
        pass

    def test_retrieve_job(self):
        """Test case for retrieve_job

        Get a job  # noqa: E501
        """
        pass

    def test_retrieve_jobs(self):
        """Test case for retrieve_jobs

        Get all jobs  # noqa: E501
        """
        pass

    def test_run_job(self):
        """Test case for run_job

        Run a job  # noqa: E501
        """
        pass

    def test_suspend_jobs(self):
        """Test case for suspend_jobs

        Suspend jobs  # noqa: E501
        """
        pass

    def test_update_job(self):
        """Test case for update_job

        Update a job  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()

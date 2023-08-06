# coding: utf-8

"""
    Kloudio APIs

"""


from __future__ import absolute_import

import unittest
import datetime

import kloudio
from kloudio.models.jobs_array import JobsArray  # noqa: E501
from kloudio.rest import ApiException

class TestJobsArray(unittest.TestCase):
    """JobsArray unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test JobsArray
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = kloudio.models.jobs_array.JobsArray()  # noqa: E501
        if include_optional :
            return JobsArray(
                job_ids = [12,1231,432]
            )
        else :
            return JobsArray(
                job_ids = [12,1231,432],
        )

    def testJobsArray(self):
        """Test JobsArray"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

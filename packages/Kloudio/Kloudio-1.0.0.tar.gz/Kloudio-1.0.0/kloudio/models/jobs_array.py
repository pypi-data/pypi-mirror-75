# coding: utf-8

"""
    Kloudio APIs

"""


import pprint
import re  # noqa: F401

import six

from kloudio.configuration import Configuration


class JobsArray(object):
    """
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'job_ids': 'list[str]'
    }

    attribute_map = {
        'job_ids': 'jobIds'
    }

    def __init__(self, job_ids=None, local_vars_configuration=None):  # noqa: E501
        """JobsArray - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._job_ids = None
        self.discriminator = None

        self.job_ids = job_ids

    @property
    def job_ids(self):
        """Gets the job_ids of this JobsArray.  # noqa: E501


        :return: The job_ids of this JobsArray.  # noqa: E501
        :rtype: list[str]
        """
        return self._job_ids

    @job_ids.setter
    def job_ids(self, job_ids):
        """Sets the job_ids of this JobsArray.


        :param job_ids: The job_ids of this JobsArray.  # noqa: E501
        :type job_ids: list[str]
        """
        if self.local_vars_configuration.client_side_validation and job_ids is None:  # noqa: E501
            raise ValueError("Invalid value for `job_ids`, must not be `None`")  # noqa: E501

        self._job_ids = job_ids

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, JobsArray):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, JobsArray):
            return True

        return self.to_dict() != other.to_dict()

# coding: utf-8

"""
    Kloudio APIs

"""


import pprint
import re  # noqa: F401

import six

from kloudio.configuration import Configuration


class RunReport(object):
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
        '_query_params': 'object',
        'preview_rows': 'float'
    }

    attribute_map = {
        '_query_params': 'queryParams',
        'preview_rows': 'previewRows'
    }

    def __init__(self, _query_params=None, preview_rows=None, local_vars_configuration=None):  # noqa: E501
        """RunReport - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self.__query_params = None
        self._preview_rows = None
        self.discriminator = None

        if _query_params is not None:
            self._query_params = _query_params
        if preview_rows is not None:
            self.preview_rows = preview_rows

    @property
    def _query_params(self):
        """Gets the _query_params of this RunReport.  # noqa: E501


        :return: The _query_params of this RunReport.  # noqa: E501
        :rtype: object
        """
        return self.__query_params

    @_query_params.setter
    def _query_params(self, _query_params):
        """Sets the _query_params of this RunReport.


        :param _query_params: The _query_params of this RunReport.  # noqa: E501
        :type _query_params: object
        """

        self.__query_params = _query_params

    @property
    def preview_rows(self):
        """Gets the preview_rows of this RunReport.  # noqa: E501


        :return: The preview_rows of this RunReport.  # noqa: E501
        :rtype: float
        """
        return self._preview_rows

    @preview_rows.setter
    def preview_rows(self, preview_rows):
        """Sets the preview_rows of this RunReport.


        :param preview_rows: The preview_rows of this RunReport.  # noqa: E501
        :type preview_rows: float
        """

        self._preview_rows = preview_rows

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
        if not isinstance(other, RunReport):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RunReport):
            return True

        return self.to_dict() != other.to_dict()

# coding: utf-8

"""
    Kloudio APIs

"""


import pprint
import re  # noqa: F401

import six

from kloudio.configuration import Configuration


class ReportShareResponse(object):
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
        'id': 'str',
        'object': 'str',
        'shared_with': 'object'
    }

    attribute_map = {
        'id': 'id',
        'object': 'object',
        'shared_with': 'sharedWith'
    }

    def __init__(self, id=None, object=None, shared_with=None, local_vars_configuration=None):  # noqa: E501
        """ReportShareResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._object = None
        self._shared_with = None
        self.discriminator = None

        self.id = id
        self.object = object
        self.shared_with = shared_with

    @property
    def id(self):
        """Gets the id of this ReportShareResponse.  # noqa: E501


        :return: The id of this ReportShareResponse.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ReportShareResponse.


        :param id: The id of this ReportShareResponse.  # noqa: E501
        :type id: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def object(self):
        """Gets the object of this ReportShareResponse.  # noqa: E501


        :return: The object of this ReportShareResponse.  # noqa: E501
        :rtype: str
        """
        return self._object

    @object.setter
    def object(self, object):
        """Sets the object of this ReportShareResponse.


        :param object: The object of this ReportShareResponse.  # noqa: E501
        :type object: str
        """
        if self.local_vars_configuration.client_side_validation and object is None:  # noqa: E501
            raise ValueError("Invalid value for `object`, must not be `None`")  # noqa: E501

        self._object = object

    @property
    def shared_with(self):
        """Gets the shared_with of this ReportShareResponse.  # noqa: E501


        :return: The shared_with of this ReportShareResponse.  # noqa: E501
        :rtype: object
        """
        return self._shared_with

    @shared_with.setter
    def shared_with(self, shared_with):
        """Sets the shared_with of this ReportShareResponse.


        :param shared_with: The shared_with of this ReportShareResponse.  # noqa: E501
        :type shared_with: object
        """
        if self.local_vars_configuration.client_side_validation and shared_with is None:  # noqa: E501
            raise ValueError("Invalid value for `shared_with`, must not be `None`")  # noqa: E501

        self._shared_with = shared_with

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
        if not isinstance(other, ReportShareResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ReportShareResponse):
            return True

        return self.to_dict() != other.to_dict()

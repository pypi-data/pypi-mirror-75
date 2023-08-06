# coding: utf-8

"""
    Kloudio APIs

"""


import pprint
import re  # noqa: F401

import six

from kloudio.configuration import Configuration


class ErrorResponse(object):
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
        'resource': 'str',
        'error': 'str',
        'message': 'str'
    }

    attribute_map = {
        'id': 'id',
        'resource': 'resource',
        'error': 'error',
        'message': 'message'
    }

    def __init__(self, id=None, resource=None, error=None, message=None, local_vars_configuration=None):  # noqa: E501
        """ErrorResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._resource = None
        self._error = None
        self._message = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if resource is not None:
            self.resource = resource
        self.error = error
        self.message = message

    @property
    def id(self):
        """Gets the id of this ErrorResponse.  # noqa: E501


        :return: The id of this ErrorResponse.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ErrorResponse.


        :param id: The id of this ErrorResponse.  # noqa: E501
        :type id: str
        """

        self._id = id

    @property
    def resource(self):
        """Gets the resource of this ErrorResponse.  # noqa: E501


        :return: The resource of this ErrorResponse.  # noqa: E501
        :rtype: str
        """
        return self._resource

    @resource.setter
    def resource(self, resource):
        """Sets the resource of this ErrorResponse.


        :param resource: The resource of this ErrorResponse.  # noqa: E501
        :type resource: str
        """

        self._resource = resource

    @property
    def error(self):
        """Gets the error of this ErrorResponse.  # noqa: E501


        :return: The error of this ErrorResponse.  # noqa: E501
        :rtype: str
        """
        return self._error

    @error.setter
    def error(self, error):
        """Sets the error of this ErrorResponse.


        :param error: The error of this ErrorResponse.  # noqa: E501
        :type error: str
        """
        if self.local_vars_configuration.client_side_validation and error is None:  # noqa: E501
            raise ValueError("Invalid value for `error`, must not be `None`")  # noqa: E501

        self._error = error

    @property
    def message(self):
        """Gets the message of this ErrorResponse.  # noqa: E501


        :return: The message of this ErrorResponse.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this ErrorResponse.


        :param message: The message of this ErrorResponse.  # noqa: E501
        :type message: str
        """
        if self.local_vars_configuration.client_side_validation and message is None:  # noqa: E501
            raise ValueError("Invalid value for `message`, must not be `None`")  # noqa: E501

        self._message = message

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
        if not isinstance(other, ErrorResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ErrorResponse):
            return True

        return self.to_dict() != other.to_dict()

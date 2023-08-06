# coding: utf-8

"""
    Kloudio APIs

"""


import pprint
import re  # noqa: F401

import six

from kloudio.configuration import Configuration


class ShareReport(object):
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
        'id': 'float',
        'email': 'str',
        'access': 'str'
    }

    attribute_map = {
        'id': 'id',
        'email': 'email',
        'access': 'access'
    }

    def __init__(self, id=None, email=None, access=None, local_vars_configuration=None):  # noqa: E501
        """ShareReport - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._email = None
        self._access = None
        self.discriminator = None

        self.id = id
        self.email = email
        self.access = access

    @property
    def id(self):
        """Gets the id of this ShareReport.  # noqa: E501


        :return: The id of this ShareReport.  # noqa: E501
        :rtype: float
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ShareReport.


        :param id: The id of this ShareReport.  # noqa: E501
        :type id: float
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def email(self):
        """Gets the email of this ShareReport.  # noqa: E501


        :return: The email of this ShareReport.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this ShareReport.


        :param email: The email of this ShareReport.  # noqa: E501
        :type email: str
        """
        if self.local_vars_configuration.client_side_validation and email is None:  # noqa: E501
            raise ValueError("Invalid value for `email`, must not be `None`")  # noqa: E501

        self._email = email

    @property
    def access(self):
        """Gets the access of this ShareReport.  # noqa: E501


        :return: The access of this ShareReport.  # noqa: E501
        :rtype: str
        """
        return self._access

    @access.setter
    def access(self, access):
        """Sets the access of this ShareReport.


        :param access: The access of this ShareReport.  # noqa: E501
        :type access: str
        """
        if self.local_vars_configuration.client_side_validation and access is None:  # noqa: E501
            raise ValueError("Invalid value for `access`, must not be `None`")  # noqa: E501

        self._access = access

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
        if not isinstance(other, ShareReport):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ShareReport):
            return True

        return self.to_dict() != other.to_dict()

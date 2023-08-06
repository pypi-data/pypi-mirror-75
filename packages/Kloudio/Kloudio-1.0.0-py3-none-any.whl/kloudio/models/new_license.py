# coding: utf-8

"""
    Kloudio APIs

"""


import pprint
import re  # noqa: F401

import six

from kloudio.configuration import Configuration


class NewLicense(object):
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
        'first_name': 'str',
        'last_name': 'str',
        'email': 'str',
        'role': 'str'
    }

    attribute_map = {
        'first_name': 'firstName',
        'last_name': 'lastName',
        'email': 'email',
        'role': 'role'
    }

    def __init__(self, first_name=None, last_name=None, email=None, role=None, local_vars_configuration=None):  # noqa: E501
        """NewLicense - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._first_name = None
        self._last_name = None
        self._email = None
        self._role = None
        self.discriminator = None

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role

    @property
    def first_name(self):
        """Gets the first_name of this NewLicense.  # noqa: E501

        First name  # noqa: E501

        :return: The first_name of this NewLicense.  # noqa: E501
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Sets the first_name of this NewLicense.

        First name  # noqa: E501

        :param first_name: The first_name of this NewLicense.  # noqa: E501
        :type first_name: str
        """
        if self.local_vars_configuration.client_side_validation and first_name is None:  # noqa: E501
            raise ValueError("Invalid value for `first_name`, must not be `None`")  # noqa: E501

        self._first_name = first_name

    @property
    def last_name(self):
        """Gets the last_name of this NewLicense.  # noqa: E501

        Last name  # noqa: E501

        :return: The last_name of this NewLicense.  # noqa: E501
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """Sets the last_name of this NewLicense.

        Last name  # noqa: E501

        :param last_name: The last_name of this NewLicense.  # noqa: E501
        :type last_name: str
        """
        if self.local_vars_configuration.client_side_validation and last_name is None:  # noqa: E501
            raise ValueError("Invalid value for `last_name`, must not be `None`")  # noqa: E501

        self._last_name = last_name

    @property
    def email(self):
        """Gets the email of this NewLicense.  # noqa: E501


        :return: The email of this NewLicense.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this NewLicense.


        :param email: The email of this NewLicense.  # noqa: E501
        :type email: str
        """
        if self.local_vars_configuration.client_side_validation and email is None:  # noqa: E501
            raise ValueError("Invalid value for `email`, must not be `None`")  # noqa: E501

        self._email = email

    @property
    def role(self):
        """Gets the role of this NewLicense.  # noqa: E501


        :return: The role of this NewLicense.  # noqa: E501
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """Sets the role of this NewLicense.


        :param role: The role of this NewLicense.  # noqa: E501
        :type role: str
        """
        if self.local_vars_configuration.client_side_validation and role is None:  # noqa: E501
            raise ValueError("Invalid value for `role`, must not be `None`")  # noqa: E501

        self._role = role

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
        if not isinstance(other, NewLicense):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NewLicense):
            return True

        return self.to_dict() != other.to_dict()

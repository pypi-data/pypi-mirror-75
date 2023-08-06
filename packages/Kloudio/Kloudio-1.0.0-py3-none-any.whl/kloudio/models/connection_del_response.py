# coding: utf-8

"""
    Kloudio APIs

"""


import pprint
import re  # noqa: F401

import six

from kloudio.configuration import Configuration


class ConnectionDelResponse(object):
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
        'object': 'str',
        'id': 'str',
        'deleted': 'bool'
    }

    attribute_map = {
        'object': 'object',
        'id': 'id',
        'deleted': 'deleted'
    }

    def __init__(self, object=None, id=None, deleted=None, local_vars_configuration=None):  # noqa: E501
        """ConnectionDelResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._object = None
        self._id = None
        self._deleted = None
        self.discriminator = None

        self.object = object
        self.id = id
        self.deleted = deleted

    @property
    def object(self):
        """Gets the object of this ConnectionDelResponse.  # noqa: E501


        :return: The object of this ConnectionDelResponse.  # noqa: E501
        :rtype: str
        """
        return self._object

    @object.setter
    def object(self, object):
        """Sets the object of this ConnectionDelResponse.


        :param object: The object of this ConnectionDelResponse.  # noqa: E501
        :type object: str
        """
        if self.local_vars_configuration.client_side_validation and object is None:  # noqa: E501
            raise ValueError("Invalid value for `object`, must not be `None`")  # noqa: E501

        self._object = object

    @property
    def id(self):
        """Gets the id of this ConnectionDelResponse.  # noqa: E501


        :return: The id of this ConnectionDelResponse.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ConnectionDelResponse.


        :param id: The id of this ConnectionDelResponse.  # noqa: E501
        :type id: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def deleted(self):
        """Gets the deleted of this ConnectionDelResponse.  # noqa: E501


        :return: The deleted of this ConnectionDelResponse.  # noqa: E501
        :rtype: bool
        """
        return self._deleted

    @deleted.setter
    def deleted(self, deleted):
        """Sets the deleted of this ConnectionDelResponse.


        :param deleted: The deleted of this ConnectionDelResponse.  # noqa: E501
        :type deleted: bool
        """
        if self.local_vars_configuration.client_side_validation and deleted is None:  # noqa: E501
            raise ValueError("Invalid value for `deleted`, must not be `None`")  # noqa: E501

        self._deleted = deleted

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
        if not isinstance(other, ConnectionDelResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ConnectionDelResponse):
            return True

        return self.to_dict() != other.to_dict()

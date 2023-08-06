# coding: utf-8

"""
    Kloudio APIs

"""


import pprint
import re  # noqa: F401

import six

from kloudio.configuration import Configuration


class UpdateConnection(object):
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
        'name': 'str',
        'host': 'str',
        'port': 'str',
        'database': 'str',
        'username': 'str',
        'password': 'str',
        'production': 'bool',
        'ssl': 'bool',
        'enable_tunnel': 'bool',
        'tunnel_info': 'object',
        'ssl_info': 'object'
    }

    attribute_map = {
        'name': 'name',
        'host': 'host',
        'port': 'port',
        'database': 'database',
        'username': 'username',
        'password': 'password',
        'production': 'production',
        'ssl': 'ssl',
        'enable_tunnel': 'enableTunnel',
        'tunnel_info': 'tunnelInfo',
        'ssl_info': 'sslInfo'
    }

    def __init__(self, name=None, host=None, port=None, database=None, username=None, password=None, production=None, ssl=None, enable_tunnel=None, tunnel_info=None, ssl_info=None, local_vars_configuration=None):  # noqa: E501
        """UpdateConnection - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._host = None
        self._port = None
        self._database = None
        self._username = None
        self._password = None
        self._production = None
        self._ssl = None
        self._enable_tunnel = None
        self._tunnel_info = None
        self._ssl_info = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        if database is not None:
            self.database = database
        if username is not None:
            self.username = username
        if password is not None:
            self.password = password
        if production is not None:
            self.production = production
        if ssl is not None:
            self.ssl = ssl
        if enable_tunnel is not None:
            self.enable_tunnel = enable_tunnel
        if tunnel_info is not None:
            self.tunnel_info = tunnel_info
        if ssl_info is not None:
            self.ssl_info = ssl_info

    @property
    def name(self):
        """Gets the name of this UpdateConnection.  # noqa: E501


        :return: The name of this UpdateConnection.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpdateConnection.


        :param name: The name of this UpdateConnection.  # noqa: E501
        :type name: str
        """

        self._name = name

    @property
    def host(self):
        """Gets the host of this UpdateConnection.  # noqa: E501


        :return: The host of this UpdateConnection.  # noqa: E501
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """Sets the host of this UpdateConnection.


        :param host: The host of this UpdateConnection.  # noqa: E501
        :type host: str
        """

        self._host = host

    @property
    def port(self):
        """Gets the port of this UpdateConnection.  # noqa: E501


        :return: The port of this UpdateConnection.  # noqa: E501
        :rtype: str
        """
        return self._port

    @port.setter
    def port(self, port):
        """Sets the port of this UpdateConnection.


        :param port: The port of this UpdateConnection.  # noqa: E501
        :type port: str
        """

        self._port = port

    @property
    def database(self):
        """Gets the database of this UpdateConnection.  # noqa: E501


        :return: The database of this UpdateConnection.  # noqa: E501
        :rtype: str
        """
        return self._database

    @database.setter
    def database(self, database):
        """Sets the database of this UpdateConnection.


        :param database: The database of this UpdateConnection.  # noqa: E501
        :type database: str
        """

        self._database = database

    @property
    def username(self):
        """Gets the username of this UpdateConnection.  # noqa: E501


        :return: The username of this UpdateConnection.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this UpdateConnection.


        :param username: The username of this UpdateConnection.  # noqa: E501
        :type username: str
        """

        self._username = username

    @property
    def password(self):
        """Gets the password of this UpdateConnection.  # noqa: E501


        :return: The password of this UpdateConnection.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this UpdateConnection.


        :param password: The password of this UpdateConnection.  # noqa: E501
        :type password: str
        """

        self._password = password

    @property
    def production(self):
        """Gets the production of this UpdateConnection.  # noqa: E501


        :return: The production of this UpdateConnection.  # noqa: E501
        :rtype: bool
        """
        return self._production

    @production.setter
    def production(self, production):
        """Sets the production of this UpdateConnection.


        :param production: The production of this UpdateConnection.  # noqa: E501
        :type production: bool
        """

        self._production = production

    @property
    def ssl(self):
        """Gets the ssl of this UpdateConnection.  # noqa: E501


        :return: The ssl of this UpdateConnection.  # noqa: E501
        :rtype: bool
        """
        return self._ssl

    @ssl.setter
    def ssl(self, ssl):
        """Sets the ssl of this UpdateConnection.


        :param ssl: The ssl of this UpdateConnection.  # noqa: E501
        :type ssl: bool
        """

        self._ssl = ssl

    @property
    def enable_tunnel(self):
        """Gets the enable_tunnel of this UpdateConnection.  # noqa: E501


        :return: The enable_tunnel of this UpdateConnection.  # noqa: E501
        :rtype: bool
        """
        return self._enable_tunnel

    @enable_tunnel.setter
    def enable_tunnel(self, enable_tunnel):
        """Sets the enable_tunnel of this UpdateConnection.


        :param enable_tunnel: The enable_tunnel of this UpdateConnection.  # noqa: E501
        :type enable_tunnel: bool
        """

        self._enable_tunnel = enable_tunnel

    @property
    def tunnel_info(self):
        """Gets the tunnel_info of this UpdateConnection.  # noqa: E501


        :return: The tunnel_info of this UpdateConnection.  # noqa: E501
        :rtype: object
        """
        return self._tunnel_info

    @tunnel_info.setter
    def tunnel_info(self, tunnel_info):
        """Sets the tunnel_info of this UpdateConnection.


        :param tunnel_info: The tunnel_info of this UpdateConnection.  # noqa: E501
        :type tunnel_info: object
        """

        self._tunnel_info = tunnel_info

    @property
    def ssl_info(self):
        """Gets the ssl_info of this UpdateConnection.  # noqa: E501


        :return: The ssl_info of this UpdateConnection.  # noqa: E501
        :rtype: object
        """
        return self._ssl_info

    @ssl_info.setter
    def ssl_info(self, ssl_info):
        """Sets the ssl_info of this UpdateConnection.


        :param ssl_info: The ssl_info of this UpdateConnection.  # noqa: E501
        :type ssl_info: object
        """

        self._ssl_info = ssl_info

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
        if not isinstance(other, UpdateConnection):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdateConnection):
            return True

        return self.to_dict() != other.to_dict()

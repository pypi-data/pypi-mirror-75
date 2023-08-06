# coding: utf-8

"""
    Kloudio APIs

"""


import pprint
import re  # noqa: F401

import six

from kloudio.configuration import Configuration


class ConnectionRespose(object):
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
        'name': 'str',
        'host': 'str',
        'port': 'str',
        'database': 'str',
        'username': 'str',
        'password': 'str',
        'db_type': 'str',
        'production': 'bool',
        'user': 'float',
        'updated_at': 'datetime',
        'ssl': 'bool',
        'updated_by': 'str',
        'created_at': 'datetime',
        'shared_with': 'object',
        'enable_tunnel': 'bool',
        'tunnel_info': 'object',
        'other_options': 'object',
        'fed': 'bool',
        'dw': 'bool',
        'metadata': 'str',
        'connection_type': 'str',
        'integration_user_id': 'float',
        'web_type': 'str',
        'ssl_info': 'object'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'host': 'host',
        'port': 'port',
        'database': 'database',
        'username': 'username',
        'password': 'password',
        'db_type': 'dbType',
        'production': 'production',
        'user': 'user',
        'updated_at': 'updatedAt',
        'ssl': 'ssl',
        'updated_by': 'updatedBy',
        'created_at': 'createdAt',
        'shared_with': 'sharedWith',
        'enable_tunnel': 'enableTunnel',
        'tunnel_info': 'tunnelInfo',
        'other_options': 'otherOptions',
        'fed': 'fed',
        'dw': 'dw',
        'metadata': 'metadata',
        'connection_type': 'connectionType',
        'integration_user_id': 'integrationUserId',
        'web_type': 'webType',
        'ssl_info': 'sslInfo'
    }

    def __init__(self, id=None, name=None, host=None, port=None, database=None, username=None, password=None, db_type=None, production=None, user=None, updated_at=None, ssl=None, updated_by=None, created_at=None, shared_with=None, enable_tunnel=None, tunnel_info=None, other_options=None, fed=None, dw=None, metadata=None, connection_type=None, integration_user_id=None, web_type=None, ssl_info=None, local_vars_configuration=None):  # noqa: E501
        """ConnectionRespose - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._host = None
        self._port = None
        self._database = None
        self._username = None
        self._password = None
        self._db_type = None
        self._production = None
        self._user = None
        self._updated_at = None
        self._ssl = None
        self._updated_by = None
        self._created_at = None
        self._shared_with = None
        self._enable_tunnel = None
        self._tunnel_info = None
        self._other_options = None
        self._fed = None
        self._dw = None
        self._metadata = None
        self._connection_type = None
        self._integration_user_id = None
        self._web_type = None
        self._ssl_info = None
        self.discriminator = None

        self.id = id
        self.name = name
        self.host = host
        self.port = port
        self.database = database
        if username is not None:
            self.username = username
        if password is not None:
            self.password = password
        if db_type is not None:
            self.db_type = db_type
        if production is not None:
            self.production = production
        if user is not None:
            self.user = user
        if updated_at is not None:
            self.updated_at = updated_at
        if ssl is not None:
            self.ssl = ssl
        if updated_by is not None:
            self.updated_by = updated_by
        if created_at is not None:
            self.created_at = created_at
        if shared_with is not None:
            self.shared_with = shared_with
        if enable_tunnel is not None:
            self.enable_tunnel = enable_tunnel
        if tunnel_info is not None:
            self.tunnel_info = tunnel_info
        if other_options is not None:
            self.other_options = other_options
        if fed is not None:
            self.fed = fed
        if dw is not None:
            self.dw = dw
        if metadata is not None:
            self.metadata = metadata
        if connection_type is not None:
            self.connection_type = connection_type
        if integration_user_id is not None:
            self.integration_user_id = integration_user_id
        if web_type is not None:
            self.web_type = web_type
        if ssl_info is not None:
            self.ssl_info = ssl_info

    @property
    def id(self):
        """Gets the id of this ConnectionRespose.  # noqa: E501


        :return: The id of this ConnectionRespose.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ConnectionRespose.


        :param id: The id of this ConnectionRespose.  # noqa: E501
        :type id: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this ConnectionRespose.  # noqa: E501


        :return: The name of this ConnectionRespose.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ConnectionRespose.


        :param name: The name of this ConnectionRespose.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def host(self):
        """Gets the host of this ConnectionRespose.  # noqa: E501


        :return: The host of this ConnectionRespose.  # noqa: E501
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """Sets the host of this ConnectionRespose.


        :param host: The host of this ConnectionRespose.  # noqa: E501
        :type host: str
        """
        if self.local_vars_configuration.client_side_validation and host is None:  # noqa: E501
            raise ValueError("Invalid value for `host`, must not be `None`")  # noqa: E501

        self._host = host

    @property
    def port(self):
        """Gets the port of this ConnectionRespose.  # noqa: E501


        :return: The port of this ConnectionRespose.  # noqa: E501
        :rtype: str
        """
        return self._port

    @port.setter
    def port(self, port):
        """Sets the port of this ConnectionRespose.


        :param port: The port of this ConnectionRespose.  # noqa: E501
        :type port: str
        """
        if self.local_vars_configuration.client_side_validation and port is None:  # noqa: E501
            raise ValueError("Invalid value for `port`, must not be `None`")  # noqa: E501

        self._port = port

    @property
    def database(self):
        """Gets the database of this ConnectionRespose.  # noqa: E501


        :return: The database of this ConnectionRespose.  # noqa: E501
        :rtype: str
        """
        return self._database

    @database.setter
    def database(self, database):
        """Sets the database of this ConnectionRespose.


        :param database: The database of this ConnectionRespose.  # noqa: E501
        :type database: str
        """
        if self.local_vars_configuration.client_side_validation and database is None:  # noqa: E501
            raise ValueError("Invalid value for `database`, must not be `None`")  # noqa: E501

        self._database = database

    @property
    def username(self):
        """Gets the username of this ConnectionRespose.  # noqa: E501


        :return: The username of this ConnectionRespose.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this ConnectionRespose.


        :param username: The username of this ConnectionRespose.  # noqa: E501
        :type username: str
        """

        self._username = username

    @property
    def password(self):
        """Gets the password of this ConnectionRespose.  # noqa: E501


        :return: The password of this ConnectionRespose.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this ConnectionRespose.


        :param password: The password of this ConnectionRespose.  # noqa: E501
        :type password: str
        """

        self._password = password

    @property
    def db_type(self):
        """Gets the db_type of this ConnectionRespose.  # noqa: E501


        :return: The db_type of this ConnectionRespose.  # noqa: E501
        :rtype: str
        """
        return self._db_type

    @db_type.setter
    def db_type(self, db_type):
        """Sets the db_type of this ConnectionRespose.


        :param db_type: The db_type of this ConnectionRespose.  # noqa: E501
        :type db_type: str
        """

        self._db_type = db_type

    @property
    def production(self):
        """Gets the production of this ConnectionRespose.  # noqa: E501


        :return: The production of this ConnectionRespose.  # noqa: E501
        :rtype: bool
        """
        return self._production

    @production.setter
    def production(self, production):
        """Sets the production of this ConnectionRespose.


        :param production: The production of this ConnectionRespose.  # noqa: E501
        :type production: bool
        """

        self._production = production

    @property
    def user(self):
        """Gets the user of this ConnectionRespose.  # noqa: E501


        :return: The user of this ConnectionRespose.  # noqa: E501
        :rtype: float
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this ConnectionRespose.


        :param user: The user of this ConnectionRespose.  # noqa: E501
        :type user: float
        """

        self._user = user

    @property
    def updated_at(self):
        """Gets the updated_at of this ConnectionRespose.  # noqa: E501


        :return: The updated_at of this ConnectionRespose.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this ConnectionRespose.


        :param updated_at: The updated_at of this ConnectionRespose.  # noqa: E501
        :type updated_at: datetime
        """

        self._updated_at = updated_at

    @property
    def ssl(self):
        """Gets the ssl of this ConnectionRespose.  # noqa: E501


        :return: The ssl of this ConnectionRespose.  # noqa: E501
        :rtype: bool
        """
        return self._ssl

    @ssl.setter
    def ssl(self, ssl):
        """Sets the ssl of this ConnectionRespose.


        :param ssl: The ssl of this ConnectionRespose.  # noqa: E501
        :type ssl: bool
        """

        self._ssl = ssl

    @property
    def updated_by(self):
        """Gets the updated_by of this ConnectionRespose.  # noqa: E501


        :return: The updated_by of this ConnectionRespose.  # noqa: E501
        :rtype: str
        """
        return self._updated_by

    @updated_by.setter
    def updated_by(self, updated_by):
        """Sets the updated_by of this ConnectionRespose.


        :param updated_by: The updated_by of this ConnectionRespose.  # noqa: E501
        :type updated_by: str
        """

        self._updated_by = updated_by

    @property
    def created_at(self):
        """Gets the created_at of this ConnectionRespose.  # noqa: E501


        :return: The created_at of this ConnectionRespose.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ConnectionRespose.


        :param created_at: The created_at of this ConnectionRespose.  # noqa: E501
        :type created_at: datetime
        """

        self._created_at = created_at

    @property
    def shared_with(self):
        """Gets the shared_with of this ConnectionRespose.  # noqa: E501


        :return: The shared_with of this ConnectionRespose.  # noqa: E501
        :rtype: object
        """
        return self._shared_with

    @shared_with.setter
    def shared_with(self, shared_with):
        """Sets the shared_with of this ConnectionRespose.


        :param shared_with: The shared_with of this ConnectionRespose.  # noqa: E501
        :type shared_with: object
        """

        self._shared_with = shared_with

    @property
    def enable_tunnel(self):
        """Gets the enable_tunnel of this ConnectionRespose.  # noqa: E501


        :return: The enable_tunnel of this ConnectionRespose.  # noqa: E501
        :rtype: bool
        """
        return self._enable_tunnel

    @enable_tunnel.setter
    def enable_tunnel(self, enable_tunnel):
        """Sets the enable_tunnel of this ConnectionRespose.


        :param enable_tunnel: The enable_tunnel of this ConnectionRespose.  # noqa: E501
        :type enable_tunnel: bool
        """

        self._enable_tunnel = enable_tunnel

    @property
    def tunnel_info(self):
        """Gets the tunnel_info of this ConnectionRespose.  # noqa: E501


        :return: The tunnel_info of this ConnectionRespose.  # noqa: E501
        :rtype: object
        """
        return self._tunnel_info

    @tunnel_info.setter
    def tunnel_info(self, tunnel_info):
        """Sets the tunnel_info of this ConnectionRespose.


        :param tunnel_info: The tunnel_info of this ConnectionRespose.  # noqa: E501
        :type tunnel_info: object
        """

        self._tunnel_info = tunnel_info

    @property
    def other_options(self):
        """Gets the other_options of this ConnectionRespose.  # noqa: E501


        :return: The other_options of this ConnectionRespose.  # noqa: E501
        :rtype: object
        """
        return self._other_options

    @other_options.setter
    def other_options(self, other_options):
        """Sets the other_options of this ConnectionRespose.


        :param other_options: The other_options of this ConnectionRespose.  # noqa: E501
        :type other_options: object
        """

        self._other_options = other_options

    @property
    def fed(self):
        """Gets the fed of this ConnectionRespose.  # noqa: E501


        :return: The fed of this ConnectionRespose.  # noqa: E501
        :rtype: bool
        """
        return self._fed

    @fed.setter
    def fed(self, fed):
        """Sets the fed of this ConnectionRespose.


        :param fed: The fed of this ConnectionRespose.  # noqa: E501
        :type fed: bool
        """

        self._fed = fed

    @property
    def dw(self):
        """Gets the dw of this ConnectionRespose.  # noqa: E501


        :return: The dw of this ConnectionRespose.  # noqa: E501
        :rtype: bool
        """
        return self._dw

    @dw.setter
    def dw(self, dw):
        """Sets the dw of this ConnectionRespose.


        :param dw: The dw of this ConnectionRespose.  # noqa: E501
        :type dw: bool
        """

        self._dw = dw

    @property
    def metadata(self):
        """Gets the metadata of this ConnectionRespose.  # noqa: E501


        :return: The metadata of this ConnectionRespose.  # noqa: E501
        :rtype: str
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this ConnectionRespose.


        :param metadata: The metadata of this ConnectionRespose.  # noqa: E501
        :type metadata: str
        """

        self._metadata = metadata

    @property
    def connection_type(self):
        """Gets the connection_type of this ConnectionRespose.  # noqa: E501


        :return: The connection_type of this ConnectionRespose.  # noqa: E501
        :rtype: str
        """
        return self._connection_type

    @connection_type.setter
    def connection_type(self, connection_type):
        """Sets the connection_type of this ConnectionRespose.


        :param connection_type: The connection_type of this ConnectionRespose.  # noqa: E501
        :type connection_type: str
        """

        self._connection_type = connection_type

    @property
    def integration_user_id(self):
        """Gets the integration_user_id of this ConnectionRespose.  # noqa: E501


        :return: The integration_user_id of this ConnectionRespose.  # noqa: E501
        :rtype: float
        """
        return self._integration_user_id

    @integration_user_id.setter
    def integration_user_id(self, integration_user_id):
        """Sets the integration_user_id of this ConnectionRespose.


        :param integration_user_id: The integration_user_id of this ConnectionRespose.  # noqa: E501
        :type integration_user_id: float
        """

        self._integration_user_id = integration_user_id

    @property
    def web_type(self):
        """Gets the web_type of this ConnectionRespose.  # noqa: E501


        :return: The web_type of this ConnectionRespose.  # noqa: E501
        :rtype: str
        """
        return self._web_type

    @web_type.setter
    def web_type(self, web_type):
        """Sets the web_type of this ConnectionRespose.


        :param web_type: The web_type of this ConnectionRespose.  # noqa: E501
        :type web_type: str
        """

        self._web_type = web_type

    @property
    def ssl_info(self):
        """Gets the ssl_info of this ConnectionRespose.  # noqa: E501


        :return: The ssl_info of this ConnectionRespose.  # noqa: E501
        :rtype: object
        """
        return self._ssl_info

    @ssl_info.setter
    def ssl_info(self, ssl_info):
        """Sets the ssl_info of this ConnectionRespose.


        :param ssl_info: The ssl_info of this ConnectionRespose.  # noqa: E501
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
        if not isinstance(other, ConnectionRespose):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ConnectionRespose):
            return True

        return self.to_dict() != other.to_dict()

# coding: utf-8

"""
    Kloudio APIs

"""


import pprint
import re  # noqa: F401

import six

from kloudio.configuration import Configuration


class ReportsResponse(object):
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
        'id': 'str',
        'connection_id': 'str',
        'description': 'str',
        'db_query': 'str',
        'db_table': 'str',
        'sql_mode': 'bool',
        'connection_type': 'str',
        '_query_params': 'object',
        'selected_cols': 'object',
        'available_cols': 'object',
        'shared_with': 'object',
        'db_schema': 'str',
        'tags': 'list[str]',
        'db_database': 'str',
        'joins': 'object',
        'custom_join': 'str',
        'additional_info': 'object',
        'join_tables': 'object',
        'settings': 'object',
        'model': 'object',
        'user_id': 'float',
        'updated_at': 'datetime',
        'created_at': 'datetime',
        'query_version': 'float',
        'db_type': 'str',
        'domain': 'str'
    }

    attribute_map = {
        'name': 'name',
        'id': 'id',
        'connection_id': 'connectionId',
        'description': 'description',
        'db_query': 'dbQuery',
        'db_table': 'dbTable',
        'sql_mode': 'sqlMode',
        'connection_type': 'connectionType',
        '_query_params': 'queryParams',
        'selected_cols': 'selectedCols',
        'available_cols': 'availableCols',
        'shared_with': 'sharedWith',
        'db_schema': 'dbSchema',
        'tags': 'tags',
        'db_database': 'dbDatabase',
        'joins': 'joins',
        'custom_join': 'customJoin',
        'additional_info': 'additionalInfo',
        'join_tables': 'joinTables',
        'settings': 'settings',
        'model': 'model',
        'user_id': 'userId',
        'updated_at': 'updatedAt',
        'created_at': 'createdAt',
        'query_version': 'queryVersion',
        'db_type': 'dbType',
        'domain': 'domain'
    }

    def __init__(self, name=None, id=None, connection_id=None, description=None, db_query=None, db_table=None, sql_mode=None, connection_type=None, _query_params=None, selected_cols=None, available_cols=None, shared_with=None, db_schema=None, tags=None, db_database=None, joins=None, custom_join=None, additional_info=None, join_tables=None, settings=None, model=None, user_id=None, updated_at=None, created_at=None, query_version=None, db_type=None, domain=None, local_vars_configuration=None):  # noqa: E501
        """ReportsResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._id = None
        self._connection_id = None
        self._description = None
        self._db_query = None
        self._db_table = None
        self._sql_mode = None
        self._connection_type = None
        self.__query_params = None
        self._selected_cols = None
        self._available_cols = None
        self._shared_with = None
        self._db_schema = None
        self._tags = None
        self._db_database = None
        self._joins = None
        self._custom_join = None
        self._additional_info = None
        self._join_tables = None
        self._settings = None
        self._model = None
        self._user_id = None
        self._updated_at = None
        self._created_at = None
        self._query_version = None
        self._db_type = None
        self._domain = None
        self.discriminator = None

        self.name = name
        self.id = id
        self.connection_id = connection_id
        if description is not None:
            self.description = description
        if db_query is not None:
            self.db_query = db_query
        if db_table is not None:
            self.db_table = db_table
        if sql_mode is not None:
            self.sql_mode = sql_mode
        if connection_type is not None:
            self.connection_type = connection_type
        if _query_params is not None:
            self._query_params = _query_params
        if selected_cols is not None:
            self.selected_cols = selected_cols
        if available_cols is not None:
            self.available_cols = available_cols
        if shared_with is not None:
            self.shared_with = shared_with
        if db_schema is not None:
            self.db_schema = db_schema
        if tags is not None:
            self.tags = tags
        if db_database is not None:
            self.db_database = db_database
        if joins is not None:
            self.joins = joins
        if custom_join is not None:
            self.custom_join = custom_join
        if additional_info is not None:
            self.additional_info = additional_info
        if join_tables is not None:
            self.join_tables = join_tables
        if settings is not None:
            self.settings = settings
        if model is not None:
            self.model = model
        if user_id is not None:
            self.user_id = user_id
        if updated_at is not None:
            self.updated_at = updated_at
        if created_at is not None:
            self.created_at = created_at
        if query_version is not None:
            self.query_version = query_version
        if db_type is not None:
            self.db_type = db_type
        if domain is not None:
            self.domain = domain

    @property
    def name(self):
        """Gets the name of this ReportsResponse.  # noqa: E501


        :return: The name of this ReportsResponse.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ReportsResponse.


        :param name: The name of this ReportsResponse.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def id(self):
        """Gets the id of this ReportsResponse.  # noqa: E501


        :return: The id of this ReportsResponse.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ReportsResponse.


        :param id: The id of this ReportsResponse.  # noqa: E501
        :type id: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def connection_id(self):
        """Gets the connection_id of this ReportsResponse.  # noqa: E501


        :return: The connection_id of this ReportsResponse.  # noqa: E501
        :rtype: str
        """
        return self._connection_id

    @connection_id.setter
    def connection_id(self, connection_id):
        """Sets the connection_id of this ReportsResponse.


        :param connection_id: The connection_id of this ReportsResponse.  # noqa: E501
        :type connection_id: str
        """
        if self.local_vars_configuration.client_side_validation and connection_id is None:  # noqa: E501
            raise ValueError("Invalid value for `connection_id`, must not be `None`")  # noqa: E501

        self._connection_id = connection_id

    @property
    def description(self):
        """Gets the description of this ReportsResponse.  # noqa: E501


        :return: The description of this ReportsResponse.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ReportsResponse.


        :param description: The description of this ReportsResponse.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def db_query(self):
        """Gets the db_query of this ReportsResponse.  # noqa: E501


        :return: The db_query of this ReportsResponse.  # noqa: E501
        :rtype: str
        """
        return self._db_query

    @db_query.setter
    def db_query(self, db_query):
        """Sets the db_query of this ReportsResponse.


        :param db_query: The db_query of this ReportsResponse.  # noqa: E501
        :type db_query: str
        """

        self._db_query = db_query

    @property
    def db_table(self):
        """Gets the db_table of this ReportsResponse.  # noqa: E501


        :return: The db_table of this ReportsResponse.  # noqa: E501
        :rtype: str
        """
        return self._db_table

    @db_table.setter
    def db_table(self, db_table):
        """Sets the db_table of this ReportsResponse.


        :param db_table: The db_table of this ReportsResponse.  # noqa: E501
        :type db_table: str
        """

        self._db_table = db_table

    @property
    def sql_mode(self):
        """Gets the sql_mode of this ReportsResponse.  # noqa: E501


        :return: The sql_mode of this ReportsResponse.  # noqa: E501
        :rtype: bool
        """
        return self._sql_mode

    @sql_mode.setter
    def sql_mode(self, sql_mode):
        """Sets the sql_mode of this ReportsResponse.


        :param sql_mode: The sql_mode of this ReportsResponse.  # noqa: E501
        :type sql_mode: bool
        """

        self._sql_mode = sql_mode

    @property
    def connection_type(self):
        """Gets the connection_type of this ReportsResponse.  # noqa: E501


        :return: The connection_type of this ReportsResponse.  # noqa: E501
        :rtype: str
        """
        return self._connection_type

    @connection_type.setter
    def connection_type(self, connection_type):
        """Sets the connection_type of this ReportsResponse.


        :param connection_type: The connection_type of this ReportsResponse.  # noqa: E501
        :type connection_type: str
        """

        self._connection_type = connection_type

    @property
    def _query_params(self):
        """Gets the _query_params of this ReportsResponse.  # noqa: E501


        :return: The _query_params of this ReportsResponse.  # noqa: E501
        :rtype: object
        """
        return self.__query_params

    @_query_params.setter
    def _query_params(self, _query_params):
        """Sets the _query_params of this ReportsResponse.


        :param _query_params: The _query_params of this ReportsResponse.  # noqa: E501
        :type _query_params: object
        """

        self.__query_params = _query_params

    @property
    def selected_cols(self):
        """Gets the selected_cols of this ReportsResponse.  # noqa: E501


        :return: The selected_cols of this ReportsResponse.  # noqa: E501
        :rtype: object
        """
        return self._selected_cols

    @selected_cols.setter
    def selected_cols(self, selected_cols):
        """Sets the selected_cols of this ReportsResponse.


        :param selected_cols: The selected_cols of this ReportsResponse.  # noqa: E501
        :type selected_cols: object
        """

        self._selected_cols = selected_cols

    @property
    def available_cols(self):
        """Gets the available_cols of this ReportsResponse.  # noqa: E501


        :return: The available_cols of this ReportsResponse.  # noqa: E501
        :rtype: object
        """
        return self._available_cols

    @available_cols.setter
    def available_cols(self, available_cols):
        """Sets the available_cols of this ReportsResponse.


        :param available_cols: The available_cols of this ReportsResponse.  # noqa: E501
        :type available_cols: object
        """

        self._available_cols = available_cols

    @property
    def shared_with(self):
        """Gets the shared_with of this ReportsResponse.  # noqa: E501


        :return: The shared_with of this ReportsResponse.  # noqa: E501
        :rtype: object
        """
        return self._shared_with

    @shared_with.setter
    def shared_with(self, shared_with):
        """Sets the shared_with of this ReportsResponse.


        :param shared_with: The shared_with of this ReportsResponse.  # noqa: E501
        :type shared_with: object
        """

        self._shared_with = shared_with

    @property
    def db_schema(self):
        """Gets the db_schema of this ReportsResponse.  # noqa: E501


        :return: The db_schema of this ReportsResponse.  # noqa: E501
        :rtype: str
        """
        return self._db_schema

    @db_schema.setter
    def db_schema(self, db_schema):
        """Sets the db_schema of this ReportsResponse.


        :param db_schema: The db_schema of this ReportsResponse.  # noqa: E501
        :type db_schema: str
        """

        self._db_schema = db_schema

    @property
    def tags(self):
        """Gets the tags of this ReportsResponse.  # noqa: E501


        :return: The tags of this ReportsResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this ReportsResponse.


        :param tags: The tags of this ReportsResponse.  # noqa: E501
        :type tags: list[str]
        """

        self._tags = tags

    @property
    def db_database(self):
        """Gets the db_database of this ReportsResponse.  # noqa: E501


        :return: The db_database of this ReportsResponse.  # noqa: E501
        :rtype: str
        """
        return self._db_database

    @db_database.setter
    def db_database(self, db_database):
        """Sets the db_database of this ReportsResponse.


        :param db_database: The db_database of this ReportsResponse.  # noqa: E501
        :type db_database: str
        """

        self._db_database = db_database

    @property
    def joins(self):
        """Gets the joins of this ReportsResponse.  # noqa: E501


        :return: The joins of this ReportsResponse.  # noqa: E501
        :rtype: object
        """
        return self._joins

    @joins.setter
    def joins(self, joins):
        """Sets the joins of this ReportsResponse.


        :param joins: The joins of this ReportsResponse.  # noqa: E501
        :type joins: object
        """

        self._joins = joins

    @property
    def custom_join(self):
        """Gets the custom_join of this ReportsResponse.  # noqa: E501


        :return: The custom_join of this ReportsResponse.  # noqa: E501
        :rtype: str
        """
        return self._custom_join

    @custom_join.setter
    def custom_join(self, custom_join):
        """Sets the custom_join of this ReportsResponse.


        :param custom_join: The custom_join of this ReportsResponse.  # noqa: E501
        :type custom_join: str
        """

        self._custom_join = custom_join

    @property
    def additional_info(self):
        """Gets the additional_info of this ReportsResponse.  # noqa: E501


        :return: The additional_info of this ReportsResponse.  # noqa: E501
        :rtype: object
        """
        return self._additional_info

    @additional_info.setter
    def additional_info(self, additional_info):
        """Sets the additional_info of this ReportsResponse.


        :param additional_info: The additional_info of this ReportsResponse.  # noqa: E501
        :type additional_info: object
        """

        self._additional_info = additional_info

    @property
    def join_tables(self):
        """Gets the join_tables of this ReportsResponse.  # noqa: E501


        :return: The join_tables of this ReportsResponse.  # noqa: E501
        :rtype: object
        """
        return self._join_tables

    @join_tables.setter
    def join_tables(self, join_tables):
        """Sets the join_tables of this ReportsResponse.


        :param join_tables: The join_tables of this ReportsResponse.  # noqa: E501
        :type join_tables: object
        """

        self._join_tables = join_tables

    @property
    def settings(self):
        """Gets the settings of this ReportsResponse.  # noqa: E501


        :return: The settings of this ReportsResponse.  # noqa: E501
        :rtype: object
        """
        return self._settings

    @settings.setter
    def settings(self, settings):
        """Sets the settings of this ReportsResponse.


        :param settings: The settings of this ReportsResponse.  # noqa: E501
        :type settings: object
        """

        self._settings = settings

    @property
    def model(self):
        """Gets the model of this ReportsResponse.  # noqa: E501


        :return: The model of this ReportsResponse.  # noqa: E501
        :rtype: object
        """
        return self._model

    @model.setter
    def model(self, model):
        """Sets the model of this ReportsResponse.


        :param model: The model of this ReportsResponse.  # noqa: E501
        :type model: object
        """

        self._model = model

    @property
    def user_id(self):
        """Gets the user_id of this ReportsResponse.  # noqa: E501


        :return: The user_id of this ReportsResponse.  # noqa: E501
        :rtype: float
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this ReportsResponse.


        :param user_id: The user_id of this ReportsResponse.  # noqa: E501
        :type user_id: float
        """

        self._user_id = user_id

    @property
    def updated_at(self):
        """Gets the updated_at of this ReportsResponse.  # noqa: E501


        :return: The updated_at of this ReportsResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this ReportsResponse.


        :param updated_at: The updated_at of this ReportsResponse.  # noqa: E501
        :type updated_at: datetime
        """

        self._updated_at = updated_at

    @property
    def created_at(self):
        """Gets the created_at of this ReportsResponse.  # noqa: E501


        :return: The created_at of this ReportsResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ReportsResponse.


        :param created_at: The created_at of this ReportsResponse.  # noqa: E501
        :type created_at: datetime
        """

        self._created_at = created_at

    @property
    def query_version(self):
        """Gets the query_version of this ReportsResponse.  # noqa: E501


        :return: The query_version of this ReportsResponse.  # noqa: E501
        :rtype: float
        """
        return self._query_version

    @query_version.setter
    def query_version(self, query_version):
        """Sets the query_version of this ReportsResponse.


        :param query_version: The query_version of this ReportsResponse.  # noqa: E501
        :type query_version: float
        """

        self._query_version = query_version

    @property
    def db_type(self):
        """Gets the db_type of this ReportsResponse.  # noqa: E501


        :return: The db_type of this ReportsResponse.  # noqa: E501
        :rtype: str
        """
        return self._db_type

    @db_type.setter
    def db_type(self, db_type):
        """Sets the db_type of this ReportsResponse.


        :param db_type: The db_type of this ReportsResponse.  # noqa: E501
        :type db_type: str
        """

        self._db_type = db_type

    @property
    def domain(self):
        """Gets the domain of this ReportsResponse.  # noqa: E501


        :return: The domain of this ReportsResponse.  # noqa: E501
        :rtype: str
        """
        return self._domain

    @domain.setter
    def domain(self, domain):
        """Sets the domain of this ReportsResponse.


        :param domain: The domain of this ReportsResponse.  # noqa: E501
        :type domain: str
        """

        self._domain = domain

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
        if not isinstance(other, ReportsResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ReportsResponse):
            return True

        return self.to_dict() != other.to_dict()

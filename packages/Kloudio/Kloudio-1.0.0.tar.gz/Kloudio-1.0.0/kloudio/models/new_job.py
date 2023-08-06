# coding: utf-8

"""
    Kloudio APIs

"""


import pprint
import re  # noqa: F401

import six

from kloudio.configuration import Configuration


class NewJob(object):
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
        'destination': 'str',
        'report_name': 'str',
        'report_id': 'str',
        'report_params': 'object',
        'frequency': 'str',
        'am_pm': 'str',
        'hour': 'str',
        'minute': 'str',
        'day': 'str',
        'description': 'str',
        'spreadsheet_id': 'str',
        'sheet_id': 'str',
        'sheet_name': 'str',
        'timezone': 'str',
        'select_cols': 'object',
        'tags': 'str',
        'email_on_success': 'bool',
        'email_on_error': 'bool',
        'metadata': 'object',
        'template_id': 'str',
        'template_name': 'str',
        'job_type': 'str'
    }

    attribute_map = {
        'destination': 'destination',
        'report_name': 'report_name',
        'report_id': 'report_id',
        'report_params': 'report_params',
        'frequency': 'frequency',
        'am_pm': 'amPm',
        'hour': 'hour',
        'minute': 'minute',
        'day': 'day',
        'description': 'description',
        'spreadsheet_id': 'spreadsheet_id',
        'sheet_id': 'sheetId',
        'sheet_name': 'sheetName',
        'timezone': 'timezone',
        'select_cols': 'select_cols',
        'tags': 'tags',
        'email_on_success': 'email_on_success',
        'email_on_error': 'email_on_error',
        'metadata': 'metadata',
        'template_id': 'templateId',
        'template_name': 'templateName',
        'job_type': 'jobType'
    }

    def __init__(self, destination=None, report_name=None, report_id=None, report_params=None, frequency=None, am_pm=None, hour=None, minute=None, day=None, description=None, spreadsheet_id=None, sheet_id=None, sheet_name=None, timezone=None, select_cols=None, tags=None, email_on_success=None, email_on_error=None, metadata=None, template_id=None, template_name=None, job_type=None, local_vars_configuration=None):  # noqa: E501
        """NewJob - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._destination = None
        self._report_name = None
        self._report_id = None
        self._report_params = None
        self._frequency = None
        self._am_pm = None
        self._hour = None
        self._minute = None
        self._day = None
        self._description = None
        self._spreadsheet_id = None
        self._sheet_id = None
        self._sheet_name = None
        self._timezone = None
        self._select_cols = None
        self._tags = None
        self._email_on_success = None
        self._email_on_error = None
        self._metadata = None
        self._template_id = None
        self._template_name = None
        self._job_type = None
        self.discriminator = None

        self.destination = destination
        self.report_name = report_name
        self.report_id = report_id
        if report_params is not None:
            self.report_params = report_params
        self.frequency = frequency
        self.am_pm = am_pm
        self.hour = hour
        self.minute = minute
        self.day = day
        if description is not None:
            self.description = description
        if spreadsheet_id is not None:
            self.spreadsheet_id = spreadsheet_id
        if sheet_id is not None:
            self.sheet_id = sheet_id
        if sheet_name is not None:
            self.sheet_name = sheet_name
        if timezone is not None:
            self.timezone = timezone
        if select_cols is not None:
            self.select_cols = select_cols
        if tags is not None:
            self.tags = tags
        if email_on_success is not None:
            self.email_on_success = email_on_success
        if email_on_error is not None:
            self.email_on_error = email_on_error
        if metadata is not None:
            self.metadata = metadata
        if template_id is not None:
            self.template_id = template_id
        if template_name is not None:
            self.template_name = template_name
        if job_type is not None:
            self.job_type = job_type

    @property
    def destination(self):
        """Gets the destination of this NewJob.  # noqa: E501


        :return: The destination of this NewJob.  # noqa: E501
        :rtype: str
        """
        return self._destination

    @destination.setter
    def destination(self, destination):
        """Sets the destination of this NewJob.


        :param destination: The destination of this NewJob.  # noqa: E501
        :type destination: str
        """
        if self.local_vars_configuration.client_side_validation and destination is None:  # noqa: E501
            raise ValueError("Invalid value for `destination`, must not be `None`")  # noqa: E501

        self._destination = destination

    @property
    def report_name(self):
        """Gets the report_name of this NewJob.  # noqa: E501


        :return: The report_name of this NewJob.  # noqa: E501
        :rtype: str
        """
        return self._report_name

    @report_name.setter
    def report_name(self, report_name):
        """Sets the report_name of this NewJob.


        :param report_name: The report_name of this NewJob.  # noqa: E501
        :type report_name: str
        """
        if self.local_vars_configuration.client_side_validation and report_name is None:  # noqa: E501
            raise ValueError("Invalid value for `report_name`, must not be `None`")  # noqa: E501

        self._report_name = report_name

    @property
    def report_id(self):
        """Gets the report_id of this NewJob.  # noqa: E501


        :return: The report_id of this NewJob.  # noqa: E501
        :rtype: str
        """
        return self._report_id

    @report_id.setter
    def report_id(self, report_id):
        """Sets the report_id of this NewJob.


        :param report_id: The report_id of this NewJob.  # noqa: E501
        :type report_id: str
        """
        if self.local_vars_configuration.client_side_validation and report_id is None:  # noqa: E501
            raise ValueError("Invalid value for `report_id`, must not be `None`")  # noqa: E501

        self._report_id = report_id

    @property
    def report_params(self):
        """Gets the report_params of this NewJob.  # noqa: E501


        :return: The report_params of this NewJob.  # noqa: E501
        :rtype: object
        """
        return self._report_params

    @report_params.setter
    def report_params(self, report_params):
        """Sets the report_params of this NewJob.


        :param report_params: The report_params of this NewJob.  # noqa: E501
        :type report_params: object
        """

        self._report_params = report_params

    @property
    def frequency(self):
        """Gets the frequency of this NewJob.  # noqa: E501


        :return: The frequency of this NewJob.  # noqa: E501
        :rtype: str
        """
        return self._frequency

    @frequency.setter
    def frequency(self, frequency):
        """Sets the frequency of this NewJob.


        :param frequency: The frequency of this NewJob.  # noqa: E501
        :type frequency: str
        """
        if self.local_vars_configuration.client_side_validation and frequency is None:  # noqa: E501
            raise ValueError("Invalid value for `frequency`, must not be `None`")  # noqa: E501

        self._frequency = frequency

    @property
    def am_pm(self):
        """Gets the am_pm of this NewJob.  # noqa: E501


        :return: The am_pm of this NewJob.  # noqa: E501
        :rtype: str
        """
        return self._am_pm

    @am_pm.setter
    def am_pm(self, am_pm):
        """Sets the am_pm of this NewJob.


        :param am_pm: The am_pm of this NewJob.  # noqa: E501
        :type am_pm: str
        """
        if self.local_vars_configuration.client_side_validation and am_pm is None:  # noqa: E501
            raise ValueError("Invalid value for `am_pm`, must not be `None`")  # noqa: E501

        self._am_pm = am_pm

    @property
    def hour(self):
        """Gets the hour of this NewJob.  # noqa: E501


        :return: The hour of this NewJob.  # noqa: E501
        :rtype: str
        """
        return self._hour

    @hour.setter
    def hour(self, hour):
        """Sets the hour of this NewJob.


        :param hour: The hour of this NewJob.  # noqa: E501
        :type hour: str
        """
        if self.local_vars_configuration.client_side_validation and hour is None:  # noqa: E501
            raise ValueError("Invalid value for `hour`, must not be `None`")  # noqa: E501

        self._hour = hour

    @property
    def minute(self):
        """Gets the minute of this NewJob.  # noqa: E501


        :return: The minute of this NewJob.  # noqa: E501
        :rtype: str
        """
        return self._minute

    @minute.setter
    def minute(self, minute):
        """Sets the minute of this NewJob.


        :param minute: The minute of this NewJob.  # noqa: E501
        :type minute: str
        """
        if self.local_vars_configuration.client_side_validation and minute is None:  # noqa: E501
            raise ValueError("Invalid value for `minute`, must not be `None`")  # noqa: E501

        self._minute = minute

    @property
    def day(self):
        """Gets the day of this NewJob.  # noqa: E501


        :return: The day of this NewJob.  # noqa: E501
        :rtype: str
        """
        return self._day

    @day.setter
    def day(self, day):
        """Sets the day of this NewJob.


        :param day: The day of this NewJob.  # noqa: E501
        :type day: str
        """
        if self.local_vars_configuration.client_side_validation and day is None:  # noqa: E501
            raise ValueError("Invalid value for `day`, must not be `None`")  # noqa: E501

        self._day = day

    @property
    def description(self):
        """Gets the description of this NewJob.  # noqa: E501


        :return: The description of this NewJob.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this NewJob.


        :param description: The description of this NewJob.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def spreadsheet_id(self):
        """Gets the spreadsheet_id of this NewJob.  # noqa: E501


        :return: The spreadsheet_id of this NewJob.  # noqa: E501
        :rtype: str
        """
        return self._spreadsheet_id

    @spreadsheet_id.setter
    def spreadsheet_id(self, spreadsheet_id):
        """Sets the spreadsheet_id of this NewJob.


        :param spreadsheet_id: The spreadsheet_id of this NewJob.  # noqa: E501
        :type spreadsheet_id: str
        """

        self._spreadsheet_id = spreadsheet_id

    @property
    def sheet_id(self):
        """Gets the sheet_id of this NewJob.  # noqa: E501


        :return: The sheet_id of this NewJob.  # noqa: E501
        :rtype: str
        """
        return self._sheet_id

    @sheet_id.setter
    def sheet_id(self, sheet_id):
        """Sets the sheet_id of this NewJob.


        :param sheet_id: The sheet_id of this NewJob.  # noqa: E501
        :type sheet_id: str
        """

        self._sheet_id = sheet_id

    @property
    def sheet_name(self):
        """Gets the sheet_name of this NewJob.  # noqa: E501


        :return: The sheet_name of this NewJob.  # noqa: E501
        :rtype: str
        """
        return self._sheet_name

    @sheet_name.setter
    def sheet_name(self, sheet_name):
        """Sets the sheet_name of this NewJob.


        :param sheet_name: The sheet_name of this NewJob.  # noqa: E501
        :type sheet_name: str
        """

        self._sheet_name = sheet_name

    @property
    def timezone(self):
        """Gets the timezone of this NewJob.  # noqa: E501


        :return: The timezone of this NewJob.  # noqa: E501
        :rtype: str
        """
        return self._timezone

    @timezone.setter
    def timezone(self, timezone):
        """Sets the timezone of this NewJob.


        :param timezone: The timezone of this NewJob.  # noqa: E501
        :type timezone: str
        """

        self._timezone = timezone

    @property
    def select_cols(self):
        """Gets the select_cols of this NewJob.  # noqa: E501


        :return: The select_cols of this NewJob.  # noqa: E501
        :rtype: object
        """
        return self._select_cols

    @select_cols.setter
    def select_cols(self, select_cols):
        """Sets the select_cols of this NewJob.


        :param select_cols: The select_cols of this NewJob.  # noqa: E501
        :type select_cols: object
        """

        self._select_cols = select_cols

    @property
    def tags(self):
        """Gets the tags of this NewJob.  # noqa: E501


        :return: The tags of this NewJob.  # noqa: E501
        :rtype: str
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this NewJob.


        :param tags: The tags of this NewJob.  # noqa: E501
        :type tags: str
        """

        self._tags = tags

    @property
    def email_on_success(self):
        """Gets the email_on_success of this NewJob.  # noqa: E501


        :return: The email_on_success of this NewJob.  # noqa: E501
        :rtype: bool
        """
        return self._email_on_success

    @email_on_success.setter
    def email_on_success(self, email_on_success):
        """Sets the email_on_success of this NewJob.


        :param email_on_success: The email_on_success of this NewJob.  # noqa: E501
        :type email_on_success: bool
        """

        self._email_on_success = email_on_success

    @property
    def email_on_error(self):
        """Gets the email_on_error of this NewJob.  # noqa: E501


        :return: The email_on_error of this NewJob.  # noqa: E501
        :rtype: bool
        """
        return self._email_on_error

    @email_on_error.setter
    def email_on_error(self, email_on_error):
        """Sets the email_on_error of this NewJob.


        :param email_on_error: The email_on_error of this NewJob.  # noqa: E501
        :type email_on_error: bool
        """

        self._email_on_error = email_on_error

    @property
    def metadata(self):
        """Gets the metadata of this NewJob.  # noqa: E501


        :return: The metadata of this NewJob.  # noqa: E501
        :rtype: object
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this NewJob.


        :param metadata: The metadata of this NewJob.  # noqa: E501
        :type metadata: object
        """

        self._metadata = metadata

    @property
    def template_id(self):
        """Gets the template_id of this NewJob.  # noqa: E501


        :return: The template_id of this NewJob.  # noqa: E501
        :rtype: str
        """
        return self._template_id

    @template_id.setter
    def template_id(self, template_id):
        """Sets the template_id of this NewJob.


        :param template_id: The template_id of this NewJob.  # noqa: E501
        :type template_id: str
        """

        self._template_id = template_id

    @property
    def template_name(self):
        """Gets the template_name of this NewJob.  # noqa: E501


        :return: The template_name of this NewJob.  # noqa: E501
        :rtype: str
        """
        return self._template_name

    @template_name.setter
    def template_name(self, template_name):
        """Sets the template_name of this NewJob.


        :param template_name: The template_name of this NewJob.  # noqa: E501
        :type template_name: str
        """

        self._template_name = template_name

    @property
    def job_type(self):
        """Gets the job_type of this NewJob.  # noqa: E501


        :return: The job_type of this NewJob.  # noqa: E501
        :rtype: str
        """
        return self._job_type

    @job_type.setter
    def job_type(self, job_type):
        """Sets the job_type of this NewJob.


        :param job_type: The job_type of this NewJob.  # noqa: E501
        :type job_type: str
        """

        self._job_type = job_type

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
        if not isinstance(other, NewJob):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NewJob):
            return True

        return self.to_dict() != other.to_dict()

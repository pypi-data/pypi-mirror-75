# coding: utf-8

"""
    Kloudio APIs

"""


from __future__ import absolute_import

import unittest

import kloudio
from kloudio.api.connections_api import ConnectionsApi  # noqa: E501
from kloudio.rest import ApiException


class TestConnectionsApi(unittest.TestCase):
    """ConnectionsApi unit test stubs"""

    def setUp(self):
        self.api = kloudio.api.connections_api.ConnectionsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_clone_connection(self):
        """Test case for clone_connection

        Clone a connection  # noqa: E501
        """
        pass

    def test_create_connection(self):
        """Test case for create_connection

        Create a connection  # noqa: E501
        """
        pass

    def test_delete_connection(self):
        """Test case for delete_connection

        Delete a connection  # noqa: E501
        """
        pass

    def test_retrieve_connection(self):
        """Test case for retrieve_connection

        Get a connection  # noqa: E501
        """
        pass

    def test_retrieve_connections(self):
        """Test case for retrieve_connections

        Get all connections  # noqa: E501
        """
        pass

    def test_share_connection(self):
        """Test case for share_connection

        Share a connection  # noqa: E501
        """
        pass

    def test_update_connection(self):
        """Test case for update_connection

        Update a connection  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()

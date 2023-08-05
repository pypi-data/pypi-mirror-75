from unittest.mock import Mock

import pytest

from koia.connector import Database


@pytest.fixture
def mock_mysql_cursor():
    mock_mysql_cursor = Mock()
    mock_mysql_cursor.execute.return_value = None
    mock_mysql_cursor.close.return_value = None
    return mock_mysql_cursor


@pytest.fixture
def mock_mysql_connect(mock_mysql_cursor):
    mock_mysql_connect = Mock()
    mock_mysql_connect.cursor.return_value = mock_mysql_cursor
    mock_mysql_connect.commit.return_value = None
    mock_mysql_connect.close.return_value = mock_mysql_cursor
    return mock_mysql_connect


@pytest.fixture
def mock_mysql(mocker, mock_mysql_connect):
    mock_mysql = mocker.patch("koia.connector.mysql.connector")
    mock_mysql.connect.return_value = mock_mysql_connect
    return mock_mysql


def test_connect(mock_mysql, mock_mysql_connect, mock_mysql_cursor, helpers):
    database_conf = helpers().database_config(
        filename="samples/database_config_sample.json"
    )
    test_connection = Database(config=database_conf)
    assert mock_mysql.connect.called
    assert mock_mysql_connect.cursor.called

    test_connection.reconnect()
    assert mock_mysql_connect.close.called
    assert mock_mysql_cursor.close.called
    assert mock_mysql.connect.call_count == 2
    assert mock_mysql_connect.cursor.call_count == 2

    test_connection.close()
    assert mock_mysql_connect.close.called
    assert mock_mysql_cursor.close.called

from typing import Dict, Generic, TypeVar

import mysql.connector

T = TypeVar("T", Dict[str, str], Dict[str, int])
X = TypeVar("X", bool, bool)


class Database(Generic[T, X]):
    """
    Create MySQLdbConnectoion instance with cursor
    """

    config: T
    autocommit: X

    def __init__(self, config: T, autocommit: X = False,) -> None:
        """Initialize connection and cursor"""
        self.config = config
        self.automcommit = autocommit
        self.connection = self._connect(autocommit=self.automcommit)
        self.cursor = self._cursor()

    def _connect(self, autocommit: X):
        """Connect to db"""
        _connection = mysql.connector.connect(**self.config)
        _connection.autocommit = autocommit
        return _connection

    def _cursor(self):
        """Create cursor"""
        _cursor = self.connection.cursor(buffered=True)
        return _cursor

    def reconnect(self):
        """Re initialize instance"""
        self.connection.close()
        self.cursor.close()
        self.__init__(config=self.config, autocommit=self.automcommit)

    def close(self):
        """Close instance session"""
        self.connection.close()
        self.cursor.close()

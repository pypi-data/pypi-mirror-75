from dataclasses import dataclass
from typing import Dict, Generic, Tuple, TypeVar

import mysql.connector


@dataclass
class ConnectorGenericTypes:
    T: TypeVar = TypeVar("T", Dict[str, str], Dict[str, int])
    X: TypeVar = TypeVar("X", bool, bool)

    def generic_types(self) -> Tuple[T, X]:
        return self.T, self.X


class Database(Generic[ConnectorGenericTypes.T, ConnectorGenericTypes.X]):
    """
    Create MySQLdbConnectoion instance with cursor
    """

    config: ConnectorGenericTypes.T
    autocommit: ConnectorGenericTypes.X

    def __init__(
        self,
        config: ConnectorGenericTypes.T,
        autocommit: ConnectorGenericTypes.X = False,
    ) -> None:
        """Initialize connection and cursor"""
        self.config = config
        self.automcommit = autocommit
        self.connection = self._connect(autocommit=self.automcommit)
        self.cursor = self._cursor()

    def _connect(self, autocommit: ConnectorGenericTypes.X):
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

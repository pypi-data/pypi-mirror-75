from __future__ import annotations

from typing import Any

from koia.connector import Database


class QueryBuilder:
    def __init__(self, database: Database) -> None:
        self.database = database
        self.query_conf: dict = {
            "where": [],
            "whereIn": [],
            "whereNotNull": [],
            "orWhere": [],
            "orderBy": [],
            "take": [],
            "innerJoin": [],
        }

    def __reload_database(self) -> None:
        """Reload database connetion"""
        self.database.reconnect()

    def table(self, table: str) -> QueryBuilder:
        """Set query table"""
        self.query_conf["table"] = table
        return self

    def where(self, column: str, operation: str, value: Any) -> QueryBuilder:
        """Set query WHERE feature"""
        self.query_conf["where"].append(f"WHERE `{column}` {operation} {value}")
        return self

    def whereIn(self, column: str, values: list) -> QueryBuilder:
        """Set query WHERE IN feature"""
        values_string = ",".join(str(value) for value in values)

        self.query_conf["whereIn"].append(f"WHERE `{column}` IN ({values_string})")
        return self

    def whereNotNull(self, column: str) -> QueryBuilder:
        """SET query WHERE NOT NULL feature"""
        self.query_conf["whereNotNull"].append(f"WHERE NOT NULL `{column}`")
        return self

    def orWhere(self, column: str, operation: str, value: Any) -> QueryBuilder:
        """SET query WHERE OR feature"""
        self.query_conf["orWhere"].append(f"OR WHERE `{column}` {operation} {value}")
        return self

    def orderBy(self, column: str, option: str) -> QueryBuilder:
        """Set query ORDER BY feature"""
        self.query_conf["orderBy"].append(f"ORDER BY `{column}` {option}")
        return self

    def take(self, count: int) -> QueryBuilder:
        """Set query LIMIT feature"""
        self.query_conf["take"].append(f"LIMIT {count}")
        return self

    def innerJoin(self, table: str, specification: dict) -> QueryBuilder:
        """Set query INNER JOIN feature"""
        query_string = f"INNER JOIN `{table}` ON "
        counter = 0

        for spec in specification.items():
            if counter == 0:
                query_string += f"({spec[0]} = {spec[1]})"
            else:
                query_string += f" and ({spec[0]} = {spec[1]})"
            counter += 1

        self.query_conf["innerJoin"].append(query_string)
        return self

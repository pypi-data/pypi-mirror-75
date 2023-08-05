import time
from typing import Dict, List, Optional

from koia.builders.utils import sort_fetched_data
from koia.database.connector import Database


class BaseModel:
    __methods__ = ["get"]
    __database__: Database
    __tablename__ = None

    def __await_db(self, error: str) -> None:
        """Sleep for a 3 second"""
        print(error)
        print("Try to reconnect after 3 sec. Zzzz...")
        time.sleep(3)

    def __orderBy(self, orderBy: dict) -> Optional[str]:
        if orderBy:
            sql_pipeline: str = ""
            for order_items in orderBy.items():
                if "ORDER BY" not in sql_pipeline:
                    sql_pipeline += f" ORDER BY {order_items[0]} {order_items[1]} "
                else:
                    sql_pipeline += f" , {order_items[0]} {order_items[1]} "

            return sql_pipeline

    def __filter(self, filter: list = "") -> Optional[str]:
        if len(filter) > 0:
            sql_pipline: str = ""

            for option in filter:
                if "WHERE" not in sql_pipline:
                    sql_pipline += f" WHERE {option} "
                else:
                    sql_pipline += f" AND {option} "

            return sql_pipline

    def __sum_query(self, *args):
        sql_pipline: str = ""
        for arg in args:
            if arg is not None:
                sql_pipline += f" {arg} "
        return sql_pipline

    def get(
        self, filter: list = "", order_by: dict = None
    ) -> Optional[Dict[str, list]]:
        sql_query: str = ""
        if self.__tablename__ is None:
            raise Exception("Unknown table name")

        columns = [
            column
            for column in dir(self)
            if "__" not in column and column not in self.__methods__
        ]

        try:
            self.__database__.connection.ping()
            sql_query += (
                f"SELECT {', '.join(f'`{column}`' for column in columns)} "
                f"FROM {self.__tablename__} "
            )
            sql_query += self.__sum_query(
                self.__filter(filter=filter), self.__orderBy(orderBy=order_by)
            )
            self.__database__.cursor.execute(sql_query)
            self.__database__.connection.commit()
            fetch: list = self.__database__.cursor.fetchall()
            field_names: list = [i[0] for i in self.__database__.cursor.description]
            sorted_data: List[Dict[str, dict]] = sort_fetched_data(
                fetch=fetch, field_names=field_names
            )

            return {"count": len(sorted_data), "fetch": sorted_data}
        except Exception as e:
            if str(e) == "2013: Lost connection to MySQL server during query":
                self.__await_db(error=str(e))
                self.__database__.reconnect()
            else:
                raise Exception(e)

import time
from typing import Dict, List, Optional

from koia.builders.utils import sort_fetched_data
from koia.database.connector import Database


class BaseModel:
    __methods__ = ["get"]
    database: Database
    __tablename__ = None

    def __await_db(self, error: str) -> None:
        """Sleep for a 3 second"""
        print(error)
        print("Try to reconnect after 3 sec. Zzzz...")
        time.sleep(3)

    def get(self) -> Optional[Dict[str, list]]:
        sql_query: str = ""
        if self.__tablename__ is None:
            raise Exception("Unknown table name")

        columns = [
            column
            for column in dir(self)
            if not column.endswith("__") and column not in self.__methods__
        ]

        try:
            self.database.connection.ping()
            sql_query += (
                f"SELECT {', '.join(f'`{column}`' for column in columns)} "
                f"FROM {self.__tablename__}"
            )
            self.database.cursor.execute(sql_query)
            self.database.connection.commit()
            fetch = self.database.cursor.fetchall()
            field_names = [i[0] for i in self.database.cursor.description]
            sorted_data: List[Dict[str, dict]] = sort_fetched_data(
                fetch=fetch, field_names=field_names
            )

            return {"count": len(sorted_data), "fetch": sorted_data}
        except Exception as e:
            if str(e) == "2013: Lost connection to MySQL server during query":
                self.__await_db(error=str(e))
                self.database.reconnect()
            else:
                raise Exception(e)

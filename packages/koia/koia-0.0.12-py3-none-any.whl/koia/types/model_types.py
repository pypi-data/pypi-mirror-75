from typing import Any, Generic

# Fix isort warnings later
from koia.types.generic_types import Float as float_generic  # noqa: F841
from koia.types.generic_types import Int  # noqa: F841
from koia.types.generic_types import Str  # noqa: F841
from koia.types.generic_types import Text as text_generic  # noqa: F841


class Column:
    def __init__(
        self,
        column_class: Any,
        pk: bool = False,
        unique: bool = False,
        autoincrement: bool = False,
    ) -> None:
        self.column_class = column_class
        self.pk = pk
        self.unique = unique
        self.autoincrement = autoincrement

    def _track_columns(self) -> None:
        pass

    def get_info(self) -> dict:
        return self.__dict__

    def __set_name__(self, _, value) -> None:
        self.__dict__["column_name"] = value


class String(Generic[Str]):
    type_of_str: str = "String"

    def __init__(self, max_length: int = 225) -> None:
        self.max_length = max_length


class Integer(Generic[Int]):
    type_of_str: str = "Integer"

    def __init__(self, max_length: int = 11) -> None:
        self.max_length = max_length


class Float(Generic[float_generic]):
    type_of_str: str = "Float"

    def __init__(self, max_length: int = 11) -> None:
        self.max_length = max_length


class Text(Generic[text_generic]):
    type_of_str: str = "Text"

    def __init__(self, max_length: int = 100) -> None:
        self.max_length = max_length

from typing import Any, Dict, Generic

# Fix isort warnings later
from koia.types.generic_types import FloatGeneric  # noqa: F841
from koia.types.generic_types import IntegerGeneric  # noqa: F841
from koia.types.generic_types import StringGeneric  # noqa: F841
from koia.types.generic_types import TextGeneric  # noqa: F841


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


class String(Generic[StringGeneric.Str]):
    type_of_str: str = "String"

    def __init__(self, max_length: int = 225) -> None:
        self.max_length = max_length

    @staticmethod
    def type_of() -> Dict[str, Any]:
        return {
            "type": type(StringGeneric().get_generictype()),
            "return_value": StringGeneric().get_generictype(),
        }


class Integer(Generic[IntegerGeneric.Int]):
    type_of_str: str = "Integer"

    def __init__(self, max_length: int = 11) -> None:
        self.max_length = max_length

    @staticmethod
    def type_of() -> Dict[str, Any]:
        return {
            "type": type(IntegerGeneric().get_generictype()),
            "return_value": IntegerGeneric().get_generictype(),
        }


class Float(Generic[FloatGeneric.Float]):
    type_of_str: str = "Float"

    def __init__(self, max_length: int = 11) -> None:
        self.max_length = max_length

    @staticmethod
    def type_of() -> Dict[str, Any]:
        return {
            "type": type(FloatGeneric().get_generictype()),
            "return_value": FloatGeneric().get_generictype(),
        }


class Text(Generic[TextGeneric.Text]):
    type_of_str: str = "Text"

    def __init__(self, max_length: int = 100) -> None:
        self.max_length = max_length

    @staticmethod
    def type_of() -> Dict[str, Any]:
        return {
            "type": type(TextGeneric().get_generictype()),
            "return_value": TextGeneric().get_generictype(),
        }

from dataclasses import dataclass
from typing import TypeVar


@dataclass
class StringGeneric:
    Str: TypeVar = TypeVar("Str", str, str)

    def get_generictype(self) -> Str:
        return self.Str


@dataclass
class IntegerGeneric:
    Int: TypeVar = TypeVar("Int", int, int)

    def get_generictype(self) -> Int:
        return self.Int


@dataclass
class FloatGeneric:
    Float: TypeVar = TypeVar("Float", float, float)

    def get_generictype(self) -> Float:
        return self.Float


@dataclass
class TextGeneric:
    Text: TypeVar = TypeVar("Text", str, str)

    def get_generictype(self) -> Text:
        return self.Text

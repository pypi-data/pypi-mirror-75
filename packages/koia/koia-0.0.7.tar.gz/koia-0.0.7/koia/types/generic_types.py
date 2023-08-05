from dataclasses import dataclass
from typing import TypeVar


@dataclass
class StringGeneric:
    Str = TypeVar("Str", str, str)

    def get_generictype(self) -> Str:
        return self.Str


@dataclass
class IntegerGeneric:
    Int = TypeVar("Int", int, int)

    def get_generictype(self) -> Int:
        return self.Int


@dataclass
class FloatGeneric:
    Float = TypeVar("Float", float, float)

    def get_generictype(self) -> Float:
        return self.Float


@dataclass
class TextGeneric:
    Text = TypeVar("Text", str, str)

    def get_generictype(self) -> Text:
        return self.Text

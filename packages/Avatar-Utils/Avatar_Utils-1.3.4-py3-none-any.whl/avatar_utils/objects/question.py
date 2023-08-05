from dataclasses import dataclass as python_dataclass, field
from typing import Any, List

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts.serializable import Serializable


@dataclass
@python_dataclass
class ChoiseQuestion(Serializable):
    options: List[Any] = field(default_factory=list)
    answers: List[Any] = field(default_factory=list)

    repr_type: str = None


@dataclass
@python_dataclass
class SelectQuestion(Serializable):
    options: List[Any] = field(default_factory=list)
    answers: List[Any] = field(default_factory=list)

    repr_type: str = None


@dataclass
@python_dataclass
class CheckBoxQuestion(Serializable):
    options: List[Any] = field(default_factory=list)
    answers: List[Any] = field(default_factory=list)

    repr_type: str = None


@dataclass
@python_dataclass
class RangeQuestion(Serializable):
    answers: List[Any] = field(default_factory=list)
    min_value: float = None
    max_value: float = None

    repr_type: str = None


@dataclass
@python_dataclass
class TextFieldQuestion(Serializable):
    answers: List[Any] = field(default_factory=list)
    shadow_title: str = None
    validation_type: str = None

    repr_type: str = None

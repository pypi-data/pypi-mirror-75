from dataclasses import dataclass as python_dataclass, field
from typing import Any, List

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts.abstract_object import AbstractObject


@dataclass
@python_dataclass
class Event(AbstractObject):
    title: str = None
    text: str = None
    origin: str = None
    deadline: str = None
    place: str = None
    tags: List[Any] = None

    repr_type: str = None

    id: int = None
    stars: int = None

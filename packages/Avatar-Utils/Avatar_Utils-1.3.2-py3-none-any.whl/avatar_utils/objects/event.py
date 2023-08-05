from dataclasses import dataclass as python_dataclass, field
from typing import Any, List

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts import AbstractResult


@dataclass
@python_dataclass
class Event(AbstractResult):
    title: str
    text: str
    origin: str
    deadline: str
    place: str
    tags: List[Any]
    sub_id: str
    stars: str
    repr_type: str = field(init=False)

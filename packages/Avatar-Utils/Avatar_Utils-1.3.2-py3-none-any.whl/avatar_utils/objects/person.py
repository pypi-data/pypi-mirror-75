from dataclasses import dataclass as python_dataclass, field
from typing import List, Any

from marshmallow_dataclass import dataclass

from avatar_utils.objects import Image
from avatar_utils.objects.abstracts.abstract_result import AbstractResult


@dataclass
@python_dataclass
class Person(AbstractResult):
    id: int
    name: str
    tags: List[Any]
    image: Image
    repr_type: str = field(init=False)

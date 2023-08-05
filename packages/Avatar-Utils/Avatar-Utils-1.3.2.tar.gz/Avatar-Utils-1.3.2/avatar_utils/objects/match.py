from dataclasses import dataclass as python_dataclass, field

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts import AbstractResult
from avatar_utils.objects.person import Person


@dataclass
@python_dataclass
class Match(AbstractResult):
    person: Person
    score: float
    repr_type: str = field(init=False)

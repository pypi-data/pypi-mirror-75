from dataclasses import dataclass as python_dataclass, field
from typing import Any, List

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts import AbstractResult


@dataclass
@python_dataclass
class Interest(AbstractResult):
    name: str
    authorlist: List[Any]
    journalInfo: str
    source: str
    repr_type: str = field(init=False)

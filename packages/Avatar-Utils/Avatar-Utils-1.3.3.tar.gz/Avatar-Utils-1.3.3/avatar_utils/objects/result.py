from dataclasses import dataclass as python_dataclass, field
from typing import List, Any

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts.serializable import Serializable


@dataclass
@python_dataclass
class Result(Serializable):
    label: str
    results: List[Any]
    repr_type: str = field(default=None)

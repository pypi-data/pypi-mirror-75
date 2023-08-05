from dataclasses import dataclass as python_dataclass
from dataclasses import field
from typing import List, Any

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts.serializable import Serializable


@dataclass
@python_dataclass
class Form(Serializable):
    label: str
    questions: List[Any]
    repr_type: str = field(init=False)

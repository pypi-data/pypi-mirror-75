from dataclasses import dataclass as python_dataclass, field
from typing import Any, Dict

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts.abstract_form import AbstractForm


@dataclass
@python_dataclass
class Question(AbstractForm):
    type: str
    options: str
    labels: Dict[Any, Any]
    repr_type: str = field(init=False)

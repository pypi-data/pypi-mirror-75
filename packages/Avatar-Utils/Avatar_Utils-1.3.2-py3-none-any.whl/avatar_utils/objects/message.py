from dataclasses import dataclass as python_dataclass, field

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts.abstract_result import AbstractResult


@dataclass
@python_dataclass
class Message(AbstractResult):
    text: str
    repr_type: str = field(default=None)

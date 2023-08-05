from dataclasses import dataclass as python_dataclass, field

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts import AbstractResult


@dataclass
@python_dataclass
class Image(AbstractResult):
    url: str
    repr_type: str = field(init=False)

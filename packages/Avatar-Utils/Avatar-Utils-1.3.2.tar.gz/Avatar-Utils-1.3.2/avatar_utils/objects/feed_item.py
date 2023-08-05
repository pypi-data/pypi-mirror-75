from dataclasses import dataclass as python_dataclass, field
from datetime import datetime

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts.serializable import Serializable
from avatar_utils.objects.form import Form
from avatar_utils.objects.result import Result


@dataclass
@python_dataclass
class FeedItem(Serializable):
    item_id: int
    importance_score: float
    header: str
    date: datetime
    type: str
    text: str
    url: str
    form: Form
    result: Result
    pinned: bool
    repr_type: str = field(init=False)

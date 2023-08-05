from datetime import datetime

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts.json_serializable import JSONSerializable


@dataclass
class FeedItem(JSONSerializable):

    def __init__(self, item_id: int,
                 importance_score: float,
                 header: str,
                 date: datetime,
                 type: str,
                 text: str,
                 url: str,
                 form: dict,
                 result: dict,
                 repr_type: str = None):
        super().__init__()
        self.item_id = item_id
        self.importance_score = importance_score
        self.header = header
        self.date = date
        self.type = type
        self.text = text
        self.url = url
        self.form = form
        self.result = result

    def __repr__(self):
        return f"""
    FeedItem: 
        item_id: {self.item_id}
        importance_score: {self.importance_score}
        header: {self.header}
        date: {self.date}
        type: {self.type}
        text: {self.text}
        url: {self.url}
        form: {self.form}
        result: {self.result}
"""

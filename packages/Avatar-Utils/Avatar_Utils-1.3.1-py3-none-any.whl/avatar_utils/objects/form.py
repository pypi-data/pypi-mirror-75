from typing import List

from avatar_utils.objects.abstracts import AbstractForm
from avatar_utils.objects.abstracts.json_serializable import JSONSerializable


class Form(JSONSerializable):

    def __init__(self, label: str, questions: List[AbstractForm], repr_type: str = None):
        super().__init__()
        self.questions = questions
        self.label = label

    def __repr__(self):
        return f"""
    FeedItem: 
        questions: {self.questions}
        label: {self.label}
"""

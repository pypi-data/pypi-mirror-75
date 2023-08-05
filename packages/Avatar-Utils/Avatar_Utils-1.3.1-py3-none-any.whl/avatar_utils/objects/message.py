from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts.abstract_result import AbstractResult

@dataclass
class Message(AbstractResult):

    def __init__(self, text: str, repr_type: str = None):
        super().__init__()
        self.text = text

    def __repr__(self):
        return f"""
    Message:
        text: {self.text}
"""

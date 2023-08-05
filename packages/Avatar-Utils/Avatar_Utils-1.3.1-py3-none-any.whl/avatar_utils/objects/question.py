from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts.abstract_form import AbstractForm


@dataclass
class Question(AbstractForm):

    def __init__(self, type: str, field: str, options: str, labels: dict, repr_type: str = None):
        super().__init__()
        self.labels = labels
        self.options = options
        self.field = field
        self.type = type

    def __repr__(self):
        return f"""
    Question:
        labels: {self.labels}
        options: {self.options}
        field: {self.field}
        type: {self.type}
"""

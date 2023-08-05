from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts import AbstractResult


@dataclass
class Article(AbstractResult):

    def __init__(self, name: str, score: float, repr_type: str = None):
        super().__init__()
        self.name = name
        self.score = score

    def __repr__(self):
        return f"""
    Article: 
        name: {self.name}
        score: {self.score}
"""

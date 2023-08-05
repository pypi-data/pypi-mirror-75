from marshmallow_dataclass import dataclass

from avatar_utils.objects.person import Person
from avatar_utils.objects.abstracts import AbstractResult


@dataclass
class Match(AbstractResult):

    def __init__(self, person: Person, score: float, repr_type: str = None):
        super().__init__()
        self.person = person
        self.score = score

    def __repr__(self):
        return f"""
    Match:
        person: {self.person}
        score: {self.score}
"""

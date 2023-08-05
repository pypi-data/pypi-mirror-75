from marshmallow_dataclass import dataclass

from avatar_utils.objects import Image
from avatar_utils.objects.abstracts.abstract_result import AbstractResult


@dataclass
class Person(AbstractResult):

    def __init__(self, id: int, name: str, tags: list, image: Image, repr_type: str = None):
        super().__init__()
        self.id = id
        self.name = name
        self.tags = tags
        self.image = image

    def __repr__(self):
        return f"""
    Person: 
        id: {self.id}
        name: {self.name}
        tags: {self.tags}
        image: {self.image}
"""

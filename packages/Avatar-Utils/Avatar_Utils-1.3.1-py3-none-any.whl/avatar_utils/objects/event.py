from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts import AbstractResult


@dataclass
class Event(AbstractResult):

    def __init__(self, title: str, text: str, origin: str, deadline: str, place: str, tags: list, sub_id: str,
                 stars: str, repr_type: str = None):
        super().__init__()
        self.text = text
        self.title = title
        self.origin = origin
        self.place = place
        self.deadline = deadline
        self.tags = tags
        self.sub_id = sub_id
        self.stars = stars

    def __repr__(self):
        return f"""
    Event: 
        text: {self.text}
        title: {self.title}
        origin: {self.origin}
        place: {self.place}
        deadline: {self.deadline}
        tags: {self.tags}
        sub_id: {self.sub_id}
        stars: {self.stars}
"""

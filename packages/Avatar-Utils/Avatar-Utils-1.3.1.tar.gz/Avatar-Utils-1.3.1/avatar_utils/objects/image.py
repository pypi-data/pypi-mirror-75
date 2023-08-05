from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts import AbstractResult


@dataclass
class Image(AbstractResult):

    def __init__(self, url: str, repr_type: str = None):
        super().__init__()
        self.url = url

    def __repr__(self):
        return f"""
    Image:
        image_url: {self.url}
"""

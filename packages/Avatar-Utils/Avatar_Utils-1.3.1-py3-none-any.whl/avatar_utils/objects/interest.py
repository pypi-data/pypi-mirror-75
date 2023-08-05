from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts import AbstractResult


@dataclass
class Interest(AbstractResult):

    def __init__(self, name: str, authorlist: list, journalInfo: str, source: str, repr_type: str = None):
        super().__init__()
        self.name = name
        self.authorlist = authorlist
        self.journalInfo = journalInfo
        self.source = source

    def __repr__(self):
        return f"""
    Interest:
        name: {self.name}
        authorlist: {self.authorlist}
        journalInfo: {self.journalInfo}
        source: {self.source}
"""

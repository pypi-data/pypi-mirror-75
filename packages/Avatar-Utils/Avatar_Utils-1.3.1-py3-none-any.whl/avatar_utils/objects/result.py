from typing import List, Any

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts import AbstractResult
from avatar_utils.objects.abstracts.json_serializable import JSONSerializable


@dataclass
class Result(JSONSerializable):
    repr_type: str
    results: List[Any]

    def __init__(self, results: List[AbstractResult], repr_type: str = None):
        super().__init__()
        self.results = results

    def __repr__(self):
        return f"""
    Result:
        results: {self.results}
"""

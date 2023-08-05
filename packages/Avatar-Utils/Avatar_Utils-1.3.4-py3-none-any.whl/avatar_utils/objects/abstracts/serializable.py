import json
from dataclasses import dataclass as python_dataclass
from typing import Any


@python_dataclass
class Serializable:
    # import avatar_utils.objects - required
    import avatar_utils.objects

    def __post_init__(self):
        self.repr_type = self.__fullname()

    # reliable but not the most productive way to serialize as a dict
    def to_dict(self):
        json_data = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

        return json.loads(json_data)

    @staticmethod
    def from_dict(data: Any):
        # import avatar_utils.objects - required
        import avatar_utils.objects

        if isinstance(data, dict):
            repr_type = data.pop('repr_type', None)

            # serializable class
            if repr_type:
                cls = eval(repr_type)

                result = {}
                for k, v in data.items():
                    result[k] = Serializable.from_dict(v)

                extracted_cls = cls(**result)
                return extracted_cls
            return data
        elif isinstance(data, list):
            i: int
            for i in range(data.__len__()):
                data[i] = Serializable.from_dict(data[i])
            return data
        else:
            return data

    def __fullname(self):
        # o.__module__ + "." + o.__class__.__qualname__ is an example in
        # this context of H.L. Mencken's "neat, plausible, and wrong."
        # Python makes no guarantees as to whether the __module__ special
        # attribute is defined, so we take a more circumspect approach.
        # Alas, the module name is explicitly excluded from __qualname__
        # in Python 3.

        module = self.__class__.__module__
        if module is None or module == str.__class__.__module__:
            return self.__class__.__name__  # Avoid reporting __builtin__
        else:
            return module + '.' + self.__class__.__name__

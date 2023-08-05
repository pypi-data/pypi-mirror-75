import json

from copy import deepcopy


class JSONSerializable:
    # source: https://medium.com/@yzhong.cs/serialize-and-deserialize-complex-json-in-python-205ecc636caa

    def __init__(self):
        self.repr_type = self.__fullname()

    def _default(self):
        return lambda o: o.to_dict()

    def to_json(self):
        return json.dumps(self, default=self._default(), sort_keys=True, indent=4)

    def to_dict(self):
        result = deepcopy(self.__dict__)

        for k, v in result.items():
            if isinstance(v, list):
                first = v[0] if v.__len__() > 0 else None
                if first and hasattr(first, 'repr_type'):
                    i: int
                    for i in range(v.__len__()):
                        v[i] = v[i].to_dict()
                else:
                    pass

            if hasattr(v, 'repr_type'):
                v = v.to_dict()

        return result

    @classmethod
    def from_json(cls, data: str):
        dict_data: dict = json.loads(data)

        return cls.from_dict(data=dict_data)

    @classmethod
    def from_dict(cls, data: dict):
        data.pop('repr_type', None)

        result = {}

        for k, v in data.items():
            if isinstance(v, list):
                first = v[0] if v.__len__() > 0 else None
                if first and isinstance(first, dict):
                    i: int
                    for i in range(v.__len__()):
                        repr_type = v[i].get('repr_type')
                        if repr_type:
                            # import avatar_utils.objects - required
                            import avatar_utils.objects
                            nested_cls = eval(repr_type)
                            v[i] = nested_cls.from_dict(data=v[i])

            if isinstance(v, dict):
                repr_type = v.get('repr_type')
                if repr_type:
                    # import avatar_utils.objects - required
                    import avatar_utils.objects
                    nested_cls = eval(repr_type)
                    v = nested_cls.from_dict(data=v)

            result[k] = v
        return cls(**result)

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

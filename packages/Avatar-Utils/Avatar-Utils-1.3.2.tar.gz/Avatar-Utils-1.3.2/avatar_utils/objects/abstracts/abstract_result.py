from dataclasses import dataclass as python_dataclass

from avatar_utils.objects.abstracts.serializable import Serializable


@python_dataclass
class AbstractResult(Serializable):
    pass

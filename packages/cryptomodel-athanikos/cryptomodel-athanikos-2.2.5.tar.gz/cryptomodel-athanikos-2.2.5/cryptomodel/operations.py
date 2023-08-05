from enum import Enum


class OPERATIONS(Enum):
    ADDED = 1
    MODIFIED = 2
    REMOVED = 3

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

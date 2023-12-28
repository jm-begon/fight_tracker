from typing import Protocol


class Intable(Protocol):
    def __int__(self) -> int:
        pass


class Boolable(Protocol):
    def __bool__(self) -> bool:
        pass

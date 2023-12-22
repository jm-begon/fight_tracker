from typing import Protocol


class Intable(Protocol):
    def __int__(self) -> int:
        pass

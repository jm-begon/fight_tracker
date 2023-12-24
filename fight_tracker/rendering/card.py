from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, NamedTuple, Self, Tuple


@dataclass
class CardSeparator:
    name: str | None = None


class KVPair(NamedTuple):
    key: str
    value: Any


class Description:
    def __init__(self, name: str | None = None) -> None:
        self.name = name
        self.items: List[KVPair] = []

    def add_item(self, key: str, value: Any) -> Self:
        if value is not None:
            self.items.append(KVPair(key, value))
        return self

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        return iter(self.items)


class Card:
    def __init__(self, title: str) -> None:
        self.title = title
        self.content: List[str] = []

    def add(self, *renderable) -> Self:
        rs = [r for r in renderable if r is not None]
        self.content.extend(rs)
        return self

    def __iter__(self):
        return iter(self.content)

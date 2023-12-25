from typing import List

import pytest

from fight_tracker.rendering import StreamRenderer


@pytest.mark.parametrize(
    ("prompt", "list_expected"),
    [
        ("abc", ["abc"]),
        ("abcd", ["abcd"]),
        ("ab cd", ["ab", "cd"]),
        ("abc def ghij", ["abc", "def", "ghij"]),
        ("abcdef", ["abcd", "ef"]),
    ],
)
def test_split_at_length_4(prompt: str, list_expected: List[str]) -> None:
    given = StreamRenderer().split_at_length(prompt, 4)
    assert list(given) == list_expected

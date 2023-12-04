import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'source/'))

import pytest
from load_allowed_words import is_valid_word


@pytest.mark.parametrize(
    "word,expected",
    [
        ("free", True),
        ("free1", False),
        ("fr", False),
        ("", False),
        ("f.R", False),
    ]
)
def test_is_valid_word(word, expected):
    assert is_valid_word(word) == expected
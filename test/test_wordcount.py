import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'source/'))

import pytest
from mock import patch
import wordcount


class MockResponse:

    def __init__(self, status_code, json):
        self.status_code = status_code
        self._json = json

    def json(self):
        return self._json


@pytest.mark.parametrize(
    "article,expected_tokens",
    [
        ("This is a test.", ["this", "is", "a", "test"]),
        ("This is a test. This is a test.", ["this", "is", "a", "test", "this", "is", "a", "test"]),
    ]
)
def test_word_tokenize_article(article, expected_tokens):
    assert wordcount.word_tokenize_article(article) == expected_tokens


@pytest.mark.parametrize(
    "word,response_json,expected_calls,expected",
    [
        ("free", {'hits': {'total': {'value': 1}}}, 1, True),
        ("free", {'hits': {'total': {'value': 0}}}, 1, False),
        ("free1", {'hits': {'total': {'value': 1}}}, 0, False),
        ("free1", {'hits': {'total': {'value': 0}}}, 0, False),
        ("fr", {'hits': {'total': {'value': 1}}}, 0, False),
        ("fr", {'hits': {'total': {'value': 0}}}, 0, False),
        ("", {'hits': {'total': {'value': 0}}}, 0, False),
    ]
)
def test_is_valid_word(word, response_json, expected_calls, expected):

    with patch('wordcount.requests.get') as mock_get:
        mock_get.return_value = MockResponse(200, response_json)
        assert wordcount.is_valid_word(word, 'localhost', 9200) == expected
        assert mock_get.call_count == expected_calls

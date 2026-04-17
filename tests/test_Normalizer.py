from utils.Normalizer import Normalizer
import pytest

def test_normalize_removes_diacritics():
     sut = Normalizer()
     assert sut.normalize_text("José Álvarez") == "jose alvarez"

def test_normalize_lowercases():
    sut = Normalizer()
    assert sut.normalize_text("JOHN DOE") == "john doe"


def test_normalize_removes_non_alphanumeric():
    sut = Normalizer()
    assert sut.normalize_text("John-Doe!@#") == "john doe"


def test_normalize_collapses_spaces():
    sut = Normalizer()
    assert sut.normalize_text("  John   Doe  ") == "john doe"


def test_normalize_empty_string():
    sut = Normalizer()
    assert sut.normalize_text("") == ""


def test_normalize_none_like_string():
    sut = Normalizer()
    assert sut.normalize_text("###") == ""


def test_tokenization_basic():
    sut = Normalizer()
    assert sut.tokenize_and_filter("john doe") == ["john", "doe"]


def test_removes_titles():
    sut = Normalizer()
    assert sut.tokenize_and_filter("mr john dr doe") == ["john", "doe"]


def test_removes_single_character_tokens():
    sut = Normalizer()
    assert sut.tokenize_and_filter("john a doe") == ["john", "doe"]


def test_removes_titles_and_single_chars_combined():
    sut = Normalizer()
    assert sut.tokenize_and_filter("mr a john o doe") == ["john", "doe"]

def test_all_tokens_filtered_out():
    sut = Normalizer()
    assert sut.tokenize_and_filter("mr dr o z a") == []

def test_empty_input():
    sut = Normalizer()
    assert sut.tokenize_and_filter("") == []

def test_perfect_match():
    sut = Normalizer()
    score = sut.get_similarity_score(
        "John Smith",
        "John Smith"
    )
    assert score == 1.0


def test_match_with_titles_and_diacritics():
    sut = Normalizer()
    score = sut.get_similarity_score(
        "Dr. José Kowalski",
        "Jose Kowalski SA"
    )
    assert score == 1.0


def test_partial_match():
    sut = Normalizer()
    score = sut.get_similarity_score(
        "Anna Kowalczyk",
        "Kowalczyk Anna Maria"
    )
    assert score - (2 / 3) < 0.0001


def test_no_match():
    sut = Normalizer()
    score = sut.get_similarity_score(
        "ABC Ltd",
        "XYZ Corp"
    )
    assert score == 0.0


def test_different_token_counts():
    sut = Normalizer()
    score = sut.get_similarity_score(
        "John Smith Brown",
        "John Smith"
    )
    assert score - (2 / 3) < 0.0001


def test_empty_entered_name():
    sut = Normalizer()
    score = sut.get_similarity_score(
        "",
        "John Smith"
    )
    assert score == 0.0


def test_empty_official_name():
    sut = Normalizer()
    score = sut.get_similarity_score(
        "John Smith",
        ""
    )
    assert score == 0.0


def test_only_titles_in_both_names():
    sut = Normalizer()
    score = sut.get_similarity_score(
        "Mr Dr",
        "Sir Prof"
    )
    assert score == 0.0
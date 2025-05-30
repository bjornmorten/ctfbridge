import pytest

from ctfbridge.models.challenge import Challenge
from ctfbridge.processors.extractors.authors import AuthorExtractor


@pytest.fixture
def extractor():
    return AuthorExtractor()


@pytest.fixture
def basic_challenge():
    return Challenge(id="test", name="Test Challenge", description="", points=100, categories=[])


def test_can_handle(extractor, basic_challenge):
    # Should not handle empty description
    assert not extractor.can_handle(basic_challenge)

    # Should not handle if already has authors
    basic_challenge.description = "Has author"
    basic_challenge.authors = ["john_doe"]
    assert not extractor.can_handle(basic_challenge)

    # Should handle if has description but no authors
    basic_challenge.authors = []
    assert extractor.can_handle(basic_challenge)


@pytest.mark.parametrize(
    "description",
    [
        "Author: john_doe",
        "author: john_doe",
        "AUTHOR: john_doe",
        "Author - john_doe",
        "Author:john_doe",
    ],
)
def test_extract_single_author(extractor, basic_challenge, description):
    basic_challenge.description = description
    result = extractor.apply(basic_challenge)
    assert result.authors == ["john_doe"]


@pytest.mark.parametrize(
    "description,expected",
    [
        ("Authors: alice, bob and charlie", ["alice", "bob", "charlie"]),
        ("Authors: alice, bob, charlie", ["alice", "bob", "charlie"]),
        ("Authors - alice and bob", ["alice", "bob"]),
        ("Authors: alice,bob,charlie", ["alice", "bob", "charlie"]),
    ],
)
def test_extract_multiple_authors(extractor, basic_challenge, description, expected):
    basic_challenge.description = description
    result = extractor.apply(basic_challenge)
    assert sorted(result.authors) == sorted(expected)


@pytest.mark.parametrize(
    "description",
    [
        "Created by john_doe",
        "created by john_doe",
        "Challenge created by john_doe",
        "This challenge was created by john_doe",
    ],
)
def test_extract_created_by(extractor, basic_challenge, description):
    basic_challenge.description = description
    result = extractor.apply(basic_challenge)
    assert result.authors == ["john_doe"]


@pytest.mark.parametrize(
    "description",
    [
        "Written by john_doe",
        "written by john_doe",
        "Challenge written by john_doe",
        "This challenge was written by john_doe",
    ],
)
def test_extract_written_by(extractor, basic_challenge, description):
    basic_challenge.description = description
    result = extractor.apply(basic_challenge)
    assert result.authors == ["john_doe"]


@pytest.mark.parametrize(
    "description",
    [
        "Made by john_doe",
        "made by john_doe",
        "Challenge made by john_doe",
        "This was made by john_doe",
    ],
)
def test_extract_made_by(extractor, basic_challenge, description):
    basic_challenge.description = description
    result = extractor.apply(basic_challenge)
    assert result.authors == ["john_doe"]


@pytest.mark.parametrize(
    "description",
    [
        "Credits: john_doe",
        "Credit: john_doe",
        "credits - john_doe",
    ],
)
def test_extract_credits(extractor, basic_challenge, description):
    basic_challenge.description = description
    result = extractor.apply(basic_challenge)
    assert result.authors == ["john_doe"]


@pytest.mark.parametrize(
    "description,expected",
    [
        ("Author: john-doe", ["john-doe"]),
        ("Author: john-doe", ["john-doe"]),
        ("Author: john_doe123", ["john_doe123"]),
        ("Authors: john-doe, jane-doe", ["john-doe", "jane-doe"]),
    ],
)
def test_handle_special_characters(extractor, basic_challenge, description, expected):
    basic_challenge.description = description
    result = extractor.apply(basic_challenge)
    assert sorted(result.authors) == sorted(expected)


def test_handle_multiple_author_mentions(extractor, basic_challenge):
    # Should use the first authors mention
    basic_challenge.description = """
    Authors: alice, bob
    Created by charlie, dave
    """
    result = extractor.apply(basic_challenge)
    assert sorted(result.authors) == ["alice", "bob"]


def test_handle_invalid_authors(extractor, basic_challenge):
    # Should ignore single-char authors
    basic_challenge.description = "Author: a"
    result = extractor.apply(basic_challenge)
    assert not result.authors


@pytest.mark.parametrize("description", ["Author:", "Author:    "])
def test_handle_errors_gracefully(extractor, basic_challenge, description):
    basic_challenge.description = description
    result = extractor.apply(basic_challenge)
    assert not result.authors  # Should not crash

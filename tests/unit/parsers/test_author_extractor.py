from ctfbridge.processors.extractors.authors import AuthorExtractor


def test_extracts_author_from_description(base_challenge):
    chal = base_challenge(description="This challenge was made by Author: alice")
    result = AuthorExtractor().apply(chal)
    assert result.author == "alice"


def test_skips_if_author_already_set(base_challenge):
    chal = base_challenge(description="Author: bob", author="carol")
    result = AuthorExtractor().apply(chal)
    assert result.author == "carol"

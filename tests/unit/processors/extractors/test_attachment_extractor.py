import pytest

from ctfbridge.models.challenge import Challenge
from ctfbridge.processors.extractors.attachments import AttachmentExtractor


@pytest.fixture
def extractor():
    return AttachmentExtractor()


@pytest.fixture
def basic_challenge():
    return Challenge(id="test", name="Test Challenge", description="", points=100, categories=[])


def test_can_handle(extractor, basic_challenge):
    # Should not handle empty description
    assert not extractor.can_handle(basic_challenge)

    # Should not handle if already has attachments
    basic_challenge.description = "Has attachment"
    basic_challenge.attachments = [{"name": "test.txt", "url": "http://example.com/test.txt"}]
    assert not extractor.can_handle(basic_challenge)

    # Should handle if has description but no attachments
    basic_challenge.attachments = []
    assert extractor.can_handle(basic_challenge)


def test_extract_basic_attachments(extractor, basic_challenge):
    basic_challenge.description = """
    Here are some files:
    - [binary](https://ctf.com/files/binary.elf)
    - https://ctf.com/files/source.zip
    <a href="https://ctf.com/files/readme.txt">readme</a>
    """

    result = extractor.apply(basic_challenge)
    assert len(result.attachments) == 3
    assert any(a.name == "binary.elf" for a in result.attachments)
    assert any(a.name == "source.zip" for a in result.attachments)
    assert any(a.name == "readme.txt" for a in result.attachments)


def test_handle_special_characters(extractor, basic_challenge):
    basic_challenge.description = """
    Download: [file with spaces](https://ctf.com/files/file%20with%20spaces.txt)
    [unicode file](https://ctf.com/files/üñîçødé_file.bin)
    """

    result = extractor.apply(basic_challenge)
    assert len(result.attachments) == 2
    assert any(a.name == "file with spaces.txt" for a in result.attachments)
    assert any(a.name == "üñîçødé_file.bin" for a in result.attachments)


def test_handle_invalid_urls(extractor, basic_challenge):
    basic_challenge.description = """
    Invalid URLs:
    - [broken](not_a_url)
    - [ftp](ftp://not/supported)
    Valid URL:
    - [valid](https://ctf.com/file.txt)
    """

    result = extractor.apply(basic_challenge)
    assert len(result.attachments) == 1
    assert result.attachments[0].name == "file.txt"


def test_handle_duplicate_urls(extractor, basic_challenge):
    basic_challenge.description = """
    Same file linked twice:
    [file](https://ctf.com/file.txt)
    [same file](https://ctf.com/file.txt)
    """

    result = extractor.apply(basic_challenge)
    assert len(result.attachments) == 1
    assert result.attachments[0].name == "file.txt"


def test_handle_errors_gracefully(extractor, basic_challenge):
    # Test with malformed URL
    basic_challenge.description = "[bad](https://[malformed)/url)"
    result = extractor.apply(basic_challenge)
    assert not result.attachments  # Should not crash

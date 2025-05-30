from urllib.parse import urlparse

import pytest

from ctfbridge.processors.helpers.url_classifier.classifier import (
    WeightConfig,
    classify_links,
    classify_url,
)
from ctfbridge.processors.helpers.url_classifier.utils import LinkClassifierContext


@pytest.fixture
def default_weights():
    return WeightConfig()


def test_classify_url_attachment(default_weights):
    # Test obvious attachment URLs
    urls = [
        "http://example.com/file.pdf",
        "https://ctf.com/downloads/challenge.zip",
        "http://files.ctf.com/resources/binary.elf",
    ]

    for url in urls:
        result = classify_url(url, default_weights)
        assert not result.is_service
        assert result.confidence >= default_weights.min_confidence
        assert result.attachment_score > result.service_score


def test_classify_url_service(default_weights):
    # Test obvious service URLs
    urls = [
        "http://localhost:8080",
        "https://service.ctf.com:1337",
        "http://127.0.0.1/api",
    ]

    for url in urls:
        result = classify_url(url, default_weights)
        assert result.is_service
        assert result.confidence >= default_weights.min_confidence
        assert result.service_score > result.attachment_score


def test_classify_url_ambiguous(default_weights):
    # Test URLs that could be either
    urls = [
        "http://ctf.com/download-service",  # Has both service and download keywords
        "https://api.ctf.com/files",  # Has both API and files indicators
    ]

    # These should be classified consistently
    results = [classify_url(url, default_weights) for url in urls]
    assert all(r.confidence < default_weights.min_confidence for r in results)


def test_classify_url_invalid():
    with pytest.raises(ValueError):
        classify_url("not_a_url")
    with pytest.raises(ValueError):
        classify_url("ftp://example.com")


def test_classify_links_mixed(default_weights):
    urls = [
        "http://example.com/file.pdf",  # Attachment
        "http://localhost:8080",  # Service
        "not_a_url",  # Invalid
        "http://ctf.com/download-service",  # Ambiguous
    ]

    result = classify_links(urls, default_weights)

    assert len(result["attachments"]) == 1
    assert len(result["services"]) == 1
    assert "http://example.com/file.pdf" in result["attachments"]
    assert "http://localhost:8080" in result["services"]

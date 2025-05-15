from ctfbridge.parsers.helpers.url_classifier import classify_links


def test_attachment_with_file_extension():
    links = ["http://example.com/file.txt"]
    result = classify_links(links)
    assert result["attachments"] == links
    assert result["services"] == []


def test_service_with_port():
    links = ["http://example.com:8080"]
    result = classify_links(links)
    assert result["services"] == links
    assert result["attachments"] == []


def test_service_hostname():
    links = ["http://localhost:1337"]
    result = classify_links(links)
    assert result["services"] == links


def test_keyword_attachment():
    links = ["http://example.com/downloads/data"]
    result = classify_links(links)
    assert result["attachments"] == links


def test_keyword_service():
    links = ["http://api.example.com/start"]
    result = classify_links(links)
    assert result["services"] == links


def test_ambiguous_prefers_service():
    links = ["http://localhost:9000/file.txt"]  # matches both
    result = classify_links(links)
    assert result["services"] == links  # service score > attachment


def test_unmatched_defaults_to_attachment():
    links = ["http://example.com/unknown"]
    result = classify_links(links)
    assert result["attachments"] == links


def test_subdomain_service():
    links = ["https://ctf.challs.example.com"]
    result = classify_links(links)
    assert result["services"] == links

import pytest

from ctfbridge.processors.helpers.url_classifier import classify_links
from ctfbridge.processors.helpers.url_classifier.classifier import classify_url


@pytest.mark.parametrize(
    "url,expected_type",
    [
        # File attachments by extension
        ("https://example.com/file.zip", "attachment"),
        ("https://example.com/file.pdf", "attachment"),
        ("https://example.com/file.exe", "attachment"),
        ("https://example.com/file.jpg", "attachment"),
        ("https://example.com/file.py", "attachment"),
        ("https://example.com/file.json", "attachment"),
        ("https://example.com/sqli.zip", "attachment"),
        ("https://example.com/sqli.tar.gz", "attachment"),
        ("https://example.com/sqli.tar", "attachment"),
        ("https://example.com/sqli.7z", "attachment"),
        ("https://example.com/web_service.zip", "attachment"),
        ("https://example.com/web_service.tar.gz", "attachment"),
        ("https://example.com/image.raw", "attachment"),
        ("https://example.com/disk.img", "attachment"),
        # Service endpoints by hostname
        ("http://localhost:8080/api", "service"),
        ("http://127.0.0.1:8000/", "service"),
        ("https://api.example.com/v1", "service"),
        ("https://app.example.com/dashboard", "service"),
        ("https://service.internal/status", "service"),
        ("https://dev.example.com/metrics", "service"),
        ("https://123.123.123.123/", "service"),
        ("https://1.2.3.4/", "service"),
        # Service endpoints by path
        ("https://example.com/api/v1/data", "service"),
        ("https://example.com/rest/users", "service"),
        ("https://example.com/graphql", "service"),
        ("https://example.com/ws/connect", "service"),
        ("https://example.com/admin/dashboard", "service"),
        ("https://example.com/health", "service"),
        ("https://example.com/index.php", "service"),
        ("https://example.com/admin/login.php", "service"),
        ("https://example.com/admin/register.php", "service"),
        ("https://example.com/login.php", "service"),
        ("https://example.com/register.php", "service"),
        ("https://example.com/index.html", "service"),
        ("https://1.2.3.4/login.php", "service"),
        ("https://1.2.3.4:12345/login.php", "service"),
        ("https://123.123.123.123/admin/", "service"),
        ("https://123.123.123.123:54321/admin/", "service"),
        # Service endpoints by cloud domains
        ("https://app.herokuapp.com/", "service"),
        ("https://api.amazonaws.com/", "service"),
        ("https://site.azurewebsites.net/", "service"),
        ("https://app.netlify.app/", "service"),
        ("https://site.vercel.app/", "service"),
        # Attachments by path
        ("https://example.com/files/data", "attachment"),
        ("https://example.com/downloads/package", "attachment"),
        ("https://example.com/attachments/doc", "attachment"),
        ("https://example.com/static/resource", "attachment"),
        ("https://example.com/releases/v1.0/binary", "attachment"),
        ("https://example.com/download/binary", "attachment"),
        ("https://example.com/files/binary", "attachment"),
        ("https://example.com/attachments/binary", "attachment"),
        ("https://example.com/attachments/binary.exe", "attachment"),
        ("https://example.com/attachments/binary.elf", "attachment"),
        ("https://example.com/attachments/binary.zip", "attachment"),
        ("https://1.2.3.4/attachment.zip", "attachment"),
        ("https://1.2.3.4/challenge.zip", "attachment"),
        ("https://123.123.123.123/web.zip", "attachment"),
        # Service endpoints by port
        ("http://example.com:8080/", "service"),
        ("http://example.com:3000/api", "service"),
        ("http://example.com:5000/", "service"),
        ("http://example.com?port=8080", "service"),
        # Cloud storage attachments
        # Google Drive
        ("https://drive.google.com/file/d/1234567890/view", "attachment"),
        ("https://docs.google.com/document/d/1234567890/edit", "attachment"),
        ("https://drive.google.com/uc?id=1234567890", "attachment"),
        # OneDrive
        ("https://1drv.ms/u/s!Abc123-xyz", "attachment"),
        ("https://onedrive.live.com/redir?resid=123456789", "attachment"),
        ("https://example.sharepoint.com/sites/CTF/Shared%20Documents/file.zip", "attachment"),
        # Dropbox
        ("https://www.dropbox.com/s/abc123xyz/file.zip", "attachment"),
        ("https://dl.dropboxusercontent.com/s/abc123xyz/file.zip", "attachment"),
        # AWS S3
        ("https://my-bucket.s3.amazonaws.com/path/to/file.zip", "attachment"),
        ("https://my-bucket.s3-us-west-2.amazonaws.com/file.zip", "attachment"),
        ("https://storage.googleapis.com/my-bucket/file.zip", "attachment"),
        ("https://my-container.blob.core.windows.net/file.zip", "attachment"),
    ],
)
def test_url_classification(url, expected_type):
    result = classify_url(url)
    if expected_type == "service":
        assert result.is_service, (
            f"Expected {url} to be classified as a service, but got attachment"
        )
    else:
        assert not result.is_service, (
            f"Expected {url} to be classified as an attachment, but got service"
        )


@pytest.mark.parametrize(
    "url",
    [
        "not_a_url",
        "ftp://example.com/file",
        "ssh://server/path",
        "file:///path/to/file",
    ],
)
def test_invalid_urls(url):
    with pytest.raises(ValueError):
        classify_url(url)


@pytest.mark.parametrize(
    "urls,expected_attachments,expected_services",
    [
        # Mixed URLs
        (
            [
                "https://example.com/file.pdf",
                "https://api.example.com/v1",
                "https://example.com/downloads/data.zip",
                "https://app.herokuapp.com/status",
            ],
            ["https://example.com/file.pdf", "https://example.com/downloads/data.zip"],
            ["https://api.example.com/v1", "https://app.herokuapp.com/status"],
        ),
        # All attachments
        (
            [
                "https://example.com/file1.pdf",
                "https://example.com/file2.zip",
                "https://example.com/downloads/file3.exe",
            ],
            [
                "https://example.com/file1.pdf",
                "https://example.com/file2.zip",
                "https://example.com/downloads/file3.exe",
            ],
            [],
        ),
        # All services
        (
            [
                "https://api.example.com/v1",
                "https://app.herokuapp.com/",
                "http://localhost:8080/graphql",
            ],
            [],
            [
                "https://api.example.com/v1",
                "https://app.herokuapp.com/",
                "http://localhost:8080/graphql",
            ],
        ),
    ],
)
def test_classify_links(urls, expected_attachments, expected_services):
    result = classify_links(urls)

    # Check attachments
    missing_attachments = set(expected_attachments) - set(result["attachments"])
    extra_attachments = set(result["attachments"]) - set(expected_attachments)
    assert not missing_attachments, f"Missing expected attachments: {missing_attachments}"
    assert not extra_attachments, f"Got unexpected attachments: {extra_attachments}"

    # Check services
    missing_services = set(expected_services) - set(result["services"])
    extra_services = set(result["services"]) - set(expected_services)
    assert not missing_services, f"Missing expected services: {missing_services}"
    assert not extra_services, f"Got unexpected services: {extra_services}"

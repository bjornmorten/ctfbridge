import pytest
import httpx  # Import httpx for AsyncClient and Response
from httpx import Response  # Specifically import Response for clarity
from urllib.parse import urlparse

from ctfbridge.platforms.ctfd.identifier import CTFdIdentifier
from ctfbridge.platforms.ctfd.http.endpoints import Endpoints  # Import Endpoints
from urllib.parse import ParseResult

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio


@pytest.fixture
async def http_client():
    """Fixture to provide an httpx.AsyncClient instance."""
    async with httpx.AsyncClient() as client:
        yield client


@pytest.fixture
async def identifier(http_client):
    """Fixture to provide a CTFdIdentifier instance."""
    return CTFdIdentifier(http_client)


# Test platform_name property
async def test_platform_name(identifier):
    assert identifier.platform_name == "CTFd"


# Test cases for match_url_pattern
@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://demo.ctfd.io/challenges", True),
        ("https://iku.ctfd.io/scoreboard", True),
        ("http://ctfd.example.com", False),
        ("https://not.ctfd.io.com", False),
        ("https://ctfd.io", False),
        ("https://example.com/ctfd/instance", False),
        ("https://someotherplatform.com", False),
        ("http://rctf.example.org", False),
    ],
)
async def test_match_url_pattern(identifier, url, expected):
    parsed_url = urlparse(url)
    assert identifier.match_url_pattern(parsed_url) == expected


# Test cases for static_detect
async def test_static_detect_success(identifier, httpx_mock):
    response_text = "<html><body>Powered by CTFd</body></html>"
    mock_response = Response(200, text=response_text)
    assert await identifier.static_detect(mock_response) is True


async def test_static_detect_failure(identifier, httpx_mock):
    response_text = "<html><body>Some other platform</body></html>"
    mock_response = Response(200, text=response_text)
    assert await identifier.static_detect(mock_response) is None


async def test_is_base_url_success(identifier, httpx_mock):
    base_url = "https://demo.ctfd.io"
    swagger_url = f"{base_url.rstrip('/')}{Endpoints.Misc.SWAGGER}"
    httpx_mock.add_response(url=swagger_url, method="GET", status_code=200, text="Swagger JSON")
    assert await identifier.is_base_url(base_url) is True


async def test_is_base_url_not_found(identifier, httpx_mock):
    base_url = "https://nonexistent.ctfd.io"
    swagger_url = f"{base_url.rstrip('/')}{Endpoints.Misc.SWAGGER}"
    httpx_mock.add_response(url=swagger_url, method="GET", status_code=404)
    assert await identifier.is_base_url(base_url) is False


async def test_is_base_url_http_error(identifier, httpx_mock):
    base_url = "https://error.ctfd.io"
    swagger_url = f"{base_url.rstrip('/')}{Endpoints.Misc.SWAGGER}"
    httpx_mock.add_exception(httpx.ConnectError("Connection failed"), url=swagger_url, method="GET")
    assert await identifier.is_base_url(base_url) is False


# Test cases for dynamic_detect
async def test_dynamic_detect_success(identifier, httpx_mock):
    base_url = "https://demo.ctfd.io"
    swagger_url = f"{base_url.rstrip('/')}{Endpoints.Misc.SWAGGER}"
    # Simulate the specific content dynamic_detect looks for
    httpx_mock.add_response(
        url=swagger_url,
        method="GET",
        status_code=200,
        text='{"...": "Endpoint to disband your current team."}',
    )
    assert await identifier.dynamic_detect(base_url) is True


async def test_dynamic_detect_wrong_content(identifier, httpx_mock):
    base_url = "https://almost.ctfd.io"
    swagger_url = f"{base_url.rstrip('/')}{Endpoints.Misc.SWAGGER}"
    httpx_mock.add_response(
        url=swagger_url, method="GET", status_code=200, text='{"info": "Not the expected content"}'
    )
    assert await identifier.dynamic_detect(base_url) is False


async def test_dynamic_detect_not_found(identifier, httpx_mock):
    base_url = "https://nonexistent.ctfd.io"
    swagger_url = f"{base_url.rstrip('/')}{Endpoints.Misc.SWAGGER}"
    httpx_mock.add_response(url=swagger_url, method="GET", status_code=404)
    assert await identifier.dynamic_detect(base_url) is False


async def test_dynamic_detect_http_error(identifier, httpx_mock):
    base_url = "https://error.ctfd.io"
    swagger_url = f"{base_url.rstrip('/')}{Endpoints.Misc.SWAGGER}"  # Use Endpoints
    httpx_mock.add_exception(httpx.ReadTimeout("Timeout"), url=swagger_url, method="GET")
    assert await identifier.dynamic_detect(base_url) is False

import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock, patch

from ctfbridge.platforms.ctfd.utils.csrf import extract_csrf_nonce, get_csrf_nonce
from ctfbridge.platforms.ctfd.http.endpoints import Endpoints

pytestmark = pytest.mark.asyncio


async def test_extract_csrf_nonce_success():
    html_with_nonce = """
    <html>
    <script type="text/javascript">
        var init = {
            'urlRoot': "/play",
            'csrfNonce': "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
            'userMode': "users",
            'userId': 0,
            'userName': null,
            'userEmail': null,
            'teamId': null,
            'teamName': null,
            'start': 1748190900,
            'end': 1751130000,
            'theme_settings': {"challenge_window_size": "norm"}
        }
    </script>
    </html>
    """
    assert (
        extract_csrf_nonce(html_with_nonce)
        == "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2"
    )


async def test_extract_csrf_nonce_different_spacing():
    html_with_nonce = """
    <script>window.csrfNonce = "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890";</script>
    <script>
    // Some other JS
    var config = {'csrfNonce':"abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"};
    // More JS
    </script>
    """  # The regex from codebase.md is specific: r"'csrfNonce':\s\"([0-9a-f]{64})\""
    # so it needs the single quotes, colon, and space.
    assert (
        extract_csrf_nonce(html_with_nonce)
        == "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
    )


async def test_extract_csrf_nonce_not_found():
    html_without_nonce = "<html><body>No nonce here.</body></html>"
    assert extract_csrf_nonce(html_without_nonce) is None


async def test_extract_csrf_nonce_malformed_script():
    html_malformed = "<html><script>var config = {'csrfNonce': unclosed_string;</script></html>"
    assert extract_csrf_nonce(html_malformed) is None


async def test_extract_csrf_nonce_empty_html():
    assert extract_csrf_nonce("") is None


async def test_get_csrf_nonce_success(httpx_mock):
    AsyncMock(spec=httpx.AsyncClient)
    nonce_value = "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2"
    html_response_text = f"<script>var config = {{'csrfNonce': \"{nonce_value}\"}};</script>"

    # Mock the client's get call
    mock_response = httpx.Response(200, text=html_response_text)

    # Create a mock client object that has a `get` method, similar to CTFdClient's structure
    mock_passed_client = MagicMock()
    mock_passed_client.get = AsyncMock(
        return_value=mock_response
    )  # This is what get_csrf_nonce calls

    # Call get_csrf_nonce with the mocked client
    extracted_nonce = await get_csrf_nonce(mock_passed_client)

    mock_passed_client.get.assert_called_once_with(Endpoints.Misc.BASE_PAGE)
    assert extracted_nonce == nonce_value


async def test_get_csrf_nonce_extraction_fails():
    mock_passed_client = MagicMock()
    mock_response = httpx.Response(200, text="<html><body>No nonce here.</body></html>")
    mock_passed_client.get = AsyncMock(return_value=mock_response)

    with pytest.raises(ValueError, match="Missing CSRF token"):
        await get_csrf_nonce(mock_passed_client)

    mock_passed_client.get.assert_called_once_with(Endpoints.Misc.BASE_PAGE)


async def test_get_csrf_nonce_http_error():
    mock_passed_client = MagicMock()
    mock_passed_client.get = AsyncMock(side_effect=httpx.RequestError("Network Error"))

    with pytest.raises(httpx.RequestError):
        await get_csrf_nonce(mock_passed_client)

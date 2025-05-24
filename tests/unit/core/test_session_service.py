import json
from unittest.mock import AsyncMock, MagicMock, mock_open, patch

import pytest

from ctfbridge.core.services.session import CoreSessionHelper
from ctfbridge.exceptions import SessionError


@pytest.fixture
def mock_client():
    mock = MagicMock()
    mock._http.headers = {}
    mock._http.cookies.set = MagicMock()
    mock._http.cookies.jar = []
    return mock


@pytest.mark.asyncio
async def test_set_token(mock_client):
    helper = CoreSessionHelper(mock_client)
    await helper.set_token("my_token")
    assert mock_client._http.headers["Authorization"] == "Bearer my_token"


@pytest.mark.asyncio
async def test_set_headers(mock_client):
    helper = CoreSessionHelper(mock_client)
    await helper.set_headers({"X-Test": "yes"})
    assert mock_client._http.headers["X-Test"] == "yes"


@pytest.mark.asyncio
async def test_set_cookie(mock_client):
    helper = CoreSessionHelper(mock_client)
    await helper.set_cookie("sessionid", "123", "example.com")
    mock_client._http.cookies.set.assert_called_with("sessionid", "123", domain="example.com")


@pytest.mark.asyncio
@patch("builtins.open", new_callable=mock_open)
@patch("json.dump")
async def test_save(mock_json_dump, mock_file, mock_client):
    cookie = MagicMock()
    cookie.name = "sid"
    cookie.value = "abc"
    cookie.domain = "example.com"
    mock_client._http.cookies.jar = [cookie]
    mock_client._http.headers = {"User-Agent": "test"}
    helper = CoreSessionHelper(mock_client)

    await helper.save("path/to/session.json")
    mock_json_dump.assert_called_once()
    mock_file.assert_called_once_with("path/to/session.json", "w")


@pytest.mark.asyncio
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data=json.dumps(
        {
            "headers": {"Authorization": "Bearer abc"},
            "cookies": [{"name": "sid", "value": "abc", "domain": "example.com"}],
        }
    ),
)
async def test_load(mock_file, mock_client):
    helper = CoreSessionHelper(mock_client)
    await helper.load("session.json")

    assert mock_client._http.headers["Authorization"] == "Bearer abc"
    mock_client._http.cookies.set.assert_called_with(name="sid", value="abc", domain="example.com")


@pytest.mark.asyncio
@patch("builtins.open", side_effect=FileNotFoundError("not found"))
async def test_load_file_not_found(mock_file, mock_client):
    helper = CoreSessionHelper(mock_client)
    with pytest.raises(SessionError) as e:
        await helper.load("missing.json")
    assert "File not found" in str(e.value)


@pytest.mark.asyncio
@patch("builtins.open", new_callable=mock_open, read_data="bad json")
async def test_load_malformed_json(mock_file, mock_client):
    with patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "bad json", 0)):
        helper = CoreSessionHelper(mock_client)
        with pytest.raises(SessionError) as e:
            await helper.load("session.json")
        assert "Malformed JSON" in str(e.value)

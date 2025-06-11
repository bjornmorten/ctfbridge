from ctfbridge import create_client
import pytest

BASE_URL = "http://localhost:8000"
URL = "http://localhost:8000"


@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "path",
    [
        "",
        "/",
        "/challenges",
        "/scoreboard",
        "/login",
        "/register",
        "/teams",
        "/api/v1/challenges",
        "/api/v1/scoreboard",
        "/some/other/path",
    ],
)
async def test_e2e_ctfd_create_client_identifies_platform(path):
    url = BASE_URL + path
    client = await create_client(url)
    assert client.platform_name == "CTFd"

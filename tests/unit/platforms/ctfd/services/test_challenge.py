import pytest
from httpx import AsyncClient, URL
from pytest_httpx import HTTPXMock

from ctfbridge.exceptions.auth import NotAuthenticatedError
from ctfbridge.exceptions.challenge import (
    ChallengeFetchError,
    ChallengeNotFoundError,
    ChallengesUnavailableError,
    SubmissionError,
)
from ctfbridge.platforms.ctfd.http.endpoints import Endpoints
from ctfbridge.platforms.ctfd.services.challenge import CTFdChallengeService
from ctfbridge.core.http import CTFBridgeClient

BASE_URL = "http://example.ctf"

# Sample challenge data for testing
SAMPLE_CHALLENGE = {
    "data": {
        "id": 1,
        "type": "standard",
        "name": "Test Challenge",
        "value": 100,
        "description": "Test description",
        "category": "web",
        "state": "visible",
        "max_attempts": 0,
        "solved": False,
    }
}

SAMPLE_CHALLENGES = {
    "data": [
        {
            "id": 1,
            "type": "standard",
            "name": "Challenge 1",
            "value": 100,
            "description": "Description 1",
            "category": "web",
            "state": "visible",
            "max_attempts": 0,
            "solved": False,
        },
        {
            "id": 2,
            "type": "standard",
            "name": "Challenge 2",
            "value": 200,
            "description": "Description 2",
            "category": "crypto",
            "state": "visible",
            "max_attempts": 0,
            "solved": True,
        },
    ]
}


class MockClient:
    def __init__(self, base_url: str = BASE_URL):
        self._http = AsyncClient(base_url=base_url)

    async def get(self, url, **kwargs):
        return await self._http.get(url, **kwargs)

    async def post(self, url, **kwargs):
        return await self._http.post(url, **kwargs)


@pytest.fixture
def http_client():
    return MockClient()


@pytest.fixture
def service(http_client):
    return CTFdChallengeService(http_client)


@pytest.mark.asyncio
async def test_fetch_challenges_success(service: CTFdChallengeService, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}{Endpoints.Challenges.LIST}",
        json=SAMPLE_CHALLENGES,
        status_code=200,
    )

    challenges = await service._fetch_challenges()
    assert len(challenges) == 2
    assert challenges[0].id == "1"
    assert challenges[0].name == "Challenge 1"
    assert challenges[0].category == "web"
    assert challenges[0].value == 100
    assert not challenges[0].solved


@pytest.mark.asyncio
async def test_fetch_challenges_unauthorized(service: CTFdChallengeService, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}{Endpoints.Challenges.LIST}",
        status_code=401,
    )

    with pytest.raises(NotAuthenticatedError):
        await service._fetch_challenges()


@pytest.mark.asyncio
async def test_fetch_challenges_unavailable(service: CTFdChallengeService, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}{Endpoints.Challenges.LIST}",
        status_code=403,
    )

    with pytest.raises(ChallengesUnavailableError):
        await service._fetch_challenges()


@pytest.mark.asyncio
async def test_fetch_challenge_by_id_success(service: CTFdChallengeService, httpx_mock: HTTPXMock):
    challenge_id = "1"
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}{Endpoints.Challenges.detail(id=challenge_id)}",
        json=SAMPLE_CHALLENGE,
        status_code=200,
    )

    challenge = await service._fetch_challenge_by_id(challenge_id)
    assert challenge.id == challenge_id
    assert challenge.name == "Test Challenge"
    assert challenge.category == "web"
    assert challenge.value == 100
    assert not challenge.solved


@pytest.mark.asyncio
async def test_fetch_challenge_by_id_not_found(
    service: CTFdChallengeService, httpx_mock: HTTPXMock
):
    challenge_id = "999"
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}{Endpoints.Challenges.detail(id=challenge_id)}",
        status_code=404,
    )

    with pytest.raises(ChallengeNotFoundError) as exc:
        await service._fetch_challenge_by_id(challenge_id)
    assert exc.value.challenge_id == challenge_id


@pytest.mark.asyncio
async def test_submit_flag_success_with_auth_header(
    service: CTFdChallengeService, httpx_mock: HTTPXMock
):
    # Setup client with auth header
    service._client._http.headers["authorization"] = "Bearer token"

    challenge_id = "1"
    flag = "flag{test}"
    response_data = {"data": {"status": "correct", "message": "Correct!"}}

    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}{Endpoints.Challenges.SUBMIT}",
        json=response_data,
        status_code=200,
    )

    result = await service.submit(challenge_id, flag)
    assert result.correct
    assert result.message == "Correct!"


@pytest.mark.asyncio
async def test_submit_flag_success_with_csrf(service: CTFdChallengeService, httpx_mock: HTTPXMock):
    challenge_id = "1"
    flag = "flag{test}"
    csrf_token = "b65d472abbf79630186f247f7566629a15cdb3353efeab522fa4eb0edb3b04e8"

    # Mock the CSRF token fetch
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}{Endpoints.Misc.BASE_PAGE}",
        text=f"""<script>'csrfNonce': "{csrf_token}",</script>""",
        status_code=200,
    )

    # Mock the submission
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}{Endpoints.Challenges.SUBMIT}",
        json={"data": {"status": "correct", "message": "Correct!"}},
        status_code=200,
    )

    result = await service.submit(challenge_id, flag)
    assert result.correct
    assert result.message == "Correct!"


@pytest.mark.asyncio
async def test_submit_flag_incorrect(service: CTFdChallengeService, httpx_mock: HTTPXMock):
    service._client._http.headers["authorization"] = "Bearer token"
    challenge_id = "1"
    flag = "wrong_flag"

    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}{Endpoints.Challenges.SUBMIT}",
        json={"data": {"status": "incorrect", "message": "Incorrect flag"}},
        status_code=200,
    )

    result = await service.submit(challenge_id, flag)
    assert not result.correct
    assert result.message == "Incorrect flag"


@pytest.mark.asyncio
async def test_submit_flag_challenge_not_found(
    service: CTFdChallengeService, httpx_mock: HTTPXMock
):
    service._client._http.headers["authorization"] = "Bearer token"
    challenge_id = "999"
    flag = "flag{test}"

    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}{Endpoints.Challenges.SUBMIT}",
        status_code=404,
    )

    with pytest.raises(ChallengeNotFoundError) as exc:
        await service.submit(challenge_id, flag)
    assert exc.value.challenge_id == challenge_id


@pytest.mark.asyncio
async def test_submit_flag_unauthorized(service: CTFdChallengeService, httpx_mock: HTTPXMock):
    service._client._http.headers["authorization"] = "Bearer token"
    challenge_id = "1"
    flag = "flag{test}"

    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}{Endpoints.Challenges.SUBMIT}",
        json={"message": ""},
        status_code=401,
        headers={"content-type": "application/json"},
    )

    with pytest.raises(NotAuthenticatedError):
        await service.submit(challenge_id, flag)


@pytest.mark.asyncio
async def test_submit_flag_invalid_response(service: CTFdChallengeService, httpx_mock: HTTPXMock):
    service._client._http.headers["authorization"] = "Bearer token"
    challenge_id = "1"
    flag = "flag{test}"

    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}{Endpoints.Challenges.SUBMIT}",
        json={"data": {}},  # Missing status field
        status_code=200,
    )

    with pytest.raises(SubmissionError) as exc:
        await service.submit(challenge_id, flag)
    assert "Missing 'status' in response" in str(exc.value)

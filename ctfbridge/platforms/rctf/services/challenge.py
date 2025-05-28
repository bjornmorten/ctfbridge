import logging
from typing import Any, Dict, List

from ctfbridge.core.services.challenge import CoreChallengeService
from ctfbridge.exceptions import ChallengeFetchError, SubmissionError
from ctfbridge.models.challenge import Attachment, Challenge
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.processors.enrich import enrich_challenge

logger = logging.getLogger(__name__)


class RCTFChallengeService(CoreChallengeService):
    def __init__(self, client):
        self._client = client

    async def get_all(
        self,
        *,
        detailed: bool = True,
        enrich: bool = True,
        solved: bool | None = None,
        min_points: int | None = None,
        max_points: int | None = None,
        category: str | None = None,
        categories: list[str] | None = None,
        tags: list[str] | None = None,
        name_contains: str | None = None,
    ) -> List[Challenge]:
        try:
            resp = await self._client._http.get(f"{self._client._platform_url}/api/v1/challs")
            data = resp.json().get("data", [])

            profile = await self._get_profile()
            solves = profile["solves"]
            solved_ids = [chal["id"] for chal in solves]
        except Exception as e:
            logger.exception("Failed to fetch challenges.")
            raise ChallengeFetchError("Invalid response format from server.") from e

        challenges = []
        for chall in data:
            challenges.append(
                Challenge(
                    id=chall["id"],
                    name=chall["name"],
                    categories=[chall["category"]],
                    value=chall["points"],
                    description=chall["description"],
                    attachments=[
                        Attachment(name=file["name"], url=file["url"]) for file in chall["files"]
                    ],
                    solved=(chall["id"] in solved_ids),
                    author=chall.get("author"),
                )
            )

        filtered_challenges = self._filter_challenges(
            challenges,
            solved=solved,
            min_points=min_points,
            max_points=max_points,
            category=category,
            categories=categories,
            tags=tags,
            name_contains=name_contains,
        )

        return filtered_challenges

    async def submit(self, challenge_id: str, flag: str) -> SubmissionResult:
        url = f"{self._client._platform_url}/api/v1/challs/{challenge_id}/submit"
        payload = {"flag": flag}

        resp = await self._client._http.post(url, json=payload)

        try:
            result = resp.json()
        except Exception:
            raise SubmissionError(
                challenge_id=challenge_id,
                flag=flag,
                reason="Unexpected response from server",
            )

        return SubmissionResult(correct=(resp.status_code == 200), message=result["message"])

    async def _get_profile(self) -> Dict[str, Any]:
        """Get user profile"""
        url = f"{self._client._platform_url}/api/v1/users/me"
        response = await self._client._http.get(url)
        data = response.json()["data"]
        return data

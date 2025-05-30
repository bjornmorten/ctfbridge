import logging
from typing import Any, Dict, List

from ctfbridge.core.services.challenge import CoreChallengeService
from ctfbridge.exceptions import ChallengeFetchError, SubmissionError
from ctfbridge.models.challenge import Attachment, Challenge
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.processors.enrich import enrich_challenge

logger = logging.getLogger(__name__)


class BergChallengeService(CoreChallengeService):
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
            resp = await self._client._http.get(f"{self._client._platform_url}/api/v2/challenges")
            data = resp.json()
        except Exception as e:
            logger.debug("Failed to fetch challenges.")
            raise ChallengeFetchError("Invalid response format from server.") from e

        challenges = []
        for chall in data:
            challenges.append(
                Challenge(
                    id=chall["name"],
                    name=chall["displayName"],
                    categories=chall["categories"],
                    description=chall["description"],
                    attachments=[
                        Attachment(name=file["fileName"], url=file["downloadUrl"])
                        for file in chall["attachments"]
                    ],
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

from typing import List
from urllib.parse import unquote, urlparse

from ctfbridge.exceptions import ChallengeFetchError, SubmissionError
from ctfbridge.models.challenge import Attachment, Challenge
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.core.services.challenge import CoreChallengeService
import re

from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


class CTFdChallengeService(CoreChallengeService):
    def __init__(self, client):
        self._client = client

    async def get_all(
        self,
        *,
        solved: bool | None = None,
        min_points: int | None = None,
        max_points: int | None = None,
        category: str | None = None,
        categories: list[str] | None = None,
        tags: list[str] | None = None,
        name_contains: str | None = None,
    ) -> List[Challenge]:
        try:
            resp = await self._client._http.get(
                f"{self._client._platform_url}/api/v1/challenges"
            )
            data = resp.json()["data"]
        except Exception as e:
            logger.exception("Failed to fetch challenges.")
            raise ChallengeFetchError("Invalid response format from server.") from e

        challenges = []
        for chal in data:
            chal_detailed = await self.get_by_id(chal["id"])
            if chal_detailed:
                challenges.append(chal_detailed)

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

    async def get_by_id(self, challenge_id: str) -> Challenge:
        try:
            resp = await self._client._http.get(
                f"{self._client._platform_url}/api/v1/challenges/{challenge_id}"
            )
            chal = resp.json()["data"]
        except Exception as e:
            logger.exception("Failed to fetch challenge ID %s", challenge_id)
            raise ChallengeFetchError("Invalid response format from server.") from e

        attachments = [
            Attachment(
                name=unquote(urlparse(url).path.split("/")[-1]),
                url=url
                if url.startswith(("http://", "https://"))
                else f"{self._client._platform_url}/{url}",
            )
            for url in chal.get("files", [])
        ]

        return Challenge(
            id=chal["id"],
            name=chal["name"],
            category=chal["category"],
            value=chal["value"],
            description=chal.get("description", ""),
            attachments=attachments,
            solved=chal.get("solved_by_me", False),
        )

    async def submit(self, challenge_id: str, flag: str) -> SubmissionResult:
        try:
            logger.debug("Fetching CSRF token from base page.")
            resp = await self._client._http.get(self._client._platform_url)
            csrf_token = self._extract_csrf_nonce(resp.text)

            logger.debug("Submitting flag for challenge ID %d", challenge_id)
            resp = await self._client._http.post(
                f"{self._client._platform_url}/api/v1/challenges/attempt",
                json={"challenge_id": challenge_id, "submission": flag},
                headers={"CSRF-Token": csrf_token},
            )

            result = resp.json()["data"]
        except Exception as e:
            logger.exception("Flag submission failed for challenge ID %s", challenge_id)
            raise SubmissionError(
                challenge_id=challenge_id,
                flag=flag,
                reason="Invalid response format from server.",
            ) from e

        return SubmissionResult(
            correct=(result["status"] == "correct"), message=result["message"]
        )

    @staticmethod
    def _extract_csrf_nonce(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        for script in soup.find_all("script"):
            if script.string and "csrfNonce" in script.string:
                match = re.search(r"'csrfNonce':\s*\"([a-fA-F0-9]+)\"", script.string)
                if match:
                    return match.group(1)
        return ""

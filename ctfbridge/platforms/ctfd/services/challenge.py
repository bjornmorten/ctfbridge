from typing import List
from urllib.parse import unquote, urlparse
from ctfbridge.parsers.enrich import enrich_challenge

from ctfbridge.exceptions import ChallengeFetchError, SubmissionError
from ctfbridge.models.challenge import Attachment, Challenge
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.core.services.challenge import CoreChallengeService

import asyncio
import logging
import re

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class CTFdChallengeService(CoreChallengeService):
    def __init__(self, client):
        self._client = client

    async def get_all(
        self,
        *,
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
            resp = await self._client._http.get(
                f"{self._client._platform_url}/api/v1/challenges"
            )
            data = resp.json().get("data", [])
        except Exception as e:
            logger.exception("Failed to fetch challenges.")
            raise ChallengeFetchError("Invalid response format from server.") from e

        challenges = await asyncio.gather(
            *(self.get_by_id(str(chal.get("id"))) for chal in data)
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

    async def get_by_id(self, challenge_id: str, enrich: bool = True) -> Challenge:
        try:
            resp = await self._client._http.get(
                f"{self._client._platform_url}/api/v1/challenges/{challenge_id}"
            )
            chal = resp.json().get("data", {})
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

        challenge = Challenge(
            id=str(chal.get("id", "")),
            name=chal.get("name", "Unnamed Challenge"),
            categories=[chal.get("category", "misc")],
            value=chal.get("value", 0),
            description=chal.get("description", ""),
            attachments=attachments,
            solved=chal.get("solved_by_me", False),
        )

        if enrich:
            challenge = enrich_challenge(challenge)

        return challenge

    async def submit(self, challenge_id: str, flag: str) -> SubmissionResult:
        try:
            logger.debug("Fetching CSRF token from base page.")
            resp = await self._client._http.get(self._client._platform_url)
            csrf_token = self._extract_csrf_nonce(resp.text)

            if not csrf_token:
                raise SubmissionError(
                    challenge_id=challenge_id,
                    flag=flag,
                    reason="Failed to extract CSRF token.",
                )

            logger.debug("Submitting flag for challenge ID %s", challenge_id)
            resp = await self._client._http.post(
                f"{self._client._platform_url}/api/v1/challenges/attempt",
                json={"challenge_id": challenge_id, "submission": flag},
                headers={"CSRF-Token": csrf_token},
            )

            result = resp.json().get("data", {})
            status = result.get("status")
            message = result.get("message", "No message provided.")

            if status is None:
                raise SubmissionError(
                    challenge_id=challenge_id,
                    flag=flag,
                    reason="Missing 'status' in submission response.",
                )

        except Exception as e:
            logger.exception("Flag submission failed for challenge ID %s", challenge_id)
            raise SubmissionError(
                challenge_id=challenge_id,
                flag=flag,
                reason="Invalid response format from server.",
            ) from e

        return SubmissionResult(correct=(status == "correct"), message=message)

    @staticmethod
    def _extract_csrf_nonce(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        for script in soup.find_all("script"):
            if script.string and "csrfNonce" in script.string:
                match = re.search(r"'csrfNonce':\s*\"([^\"]+)\"", script.string)
                if match:
                    return match.group(1)
        return ""

import logging
import re
from urllib.parse import unquote, urlparse

from bs4 import BeautifulSoup

from ctfbridge.core.services.challenge import CoreChallengeService
from ctfbridge.exceptions import ChallengeFetchError, SubmissionError
from ctfbridge.models.challenge import Attachment, Challenge
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.parsers.enrich import enrich_challenge

logger = logging.getLogger(__name__)


class CTFdChallengeService(CoreChallengeService):
    def __init__(self, client):
        self._client = client

    @property
    def base_has_details(self) -> bool:
        return False

    async def _fetch_base_challenges(self) -> list[Challenge]:
        try:
            resp = await self._client.get("challenges")
            data = resp.json().get("data", [])
            return [self._parse_challenge(chal, full=False) for chal in data]
        except Exception as e:
            logger.exception("Failed to fetch base challenges")
            raise ChallengeFetchError("Failed to fetch challenges from CTFd.") from e

    async def _fetch_challenge_by_id(self, challenge_id: str, enrich: bool = True) -> Challenge:
        try:
            resp = await self._client.get("challenge_detail", id=challenge_id)
            data = resp.json().get("data", {})
        except Exception as e:
            logger.exception("Failed to fetch challenge ID %s", challenge_id)
            raise ChallengeFetchError(f"Could not load challenge ID {challenge_id}") from e

        challenge = self._parse_challenge(data, full=True)
        return enrich_challenge(challenge) if enrich else challenge

    def _parse_challenge(self, data: dict, full: bool = False) -> Challenge:
        attachments = []
        if full:
            attachments = [
                Attachment(
                    name=unquote(urlparse(url).path.split("/")[-1]),
                    url=url
                    if url.startswith(("http://", "https://"))
                    else f"{self._client._platform_url}/{url}",
                )
                for url in data.get("files", [])
            ]

        return Challenge(
            id=str(data["id"]),
            name=data["name"],
            categories=[data["category"]] if data.get("category") else [],
            value=data.get("value"),
            description=data.get("description") if full else None,
            attachments=attachments if full else [],
            solved=data.get("solved_by_me"),
        )

    async def submit(self, challenge_id: str, flag: str) -> SubmissionResult:
        try:
            logger.debug("Fetching CSRF token from base page.")
            resp = await self._client.get("base_page")
            csrf_token = self._extract_csrf_nonce(resp.text)

            if not csrf_token:
                raise SubmissionError(
                    challenge_id=challenge_id,
                    flag=flag,
                    reason="Failed to extract CSRF token.",
                )

            logger.debug("Submitting flag for challenge ID %s", challenge_id)
            resp = await self._client.post(
                "submit",
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

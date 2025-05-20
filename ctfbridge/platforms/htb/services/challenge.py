import logging
from typing import Any, Dict, List

from ctfbridge.core.services.challenge import CoreChallengeService
from ctfbridge.exceptions import BadRequestError, ChallengeFetchError, SubmissionError
from ctfbridge.models.challenge import Attachment, Challenge
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.parsers.enrich import enrich_challenge

logger = logging.getLogger(__name__)


class HTBChallengeService(CoreChallengeService):
    def __init__(self, client):
        self._client = client
        self._category_cache: Dict[int, str] = {}

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
                self._client._get_api_url(f"ctfs/{self._client._ctf_id}")
            )
            data = resp.json()
            challenges_raw = data["challenges"]
        except Exception as e:
            logger.exception("Failed to fetch challenges.")
            raise ChallengeFetchError("Invalid response format from server.") from e

        if not self._category_cache:
            await self._get_challenge_categories()

        challenges = []
        for chall in challenges_raw:
            challenges.append(
                Challenge(
                    id=str(chall.get("id")),
                    name=chall.get("name"),
                    value=chall.get("points"),
                    difficulty=chall.get("difficulty"),
                    categories=[
                        self._category_cache[chall.get("challenge_category_id")]
                    ],
                    description=chall.get("description"),
                    attachments=(
                        [
                            Attachment(
                                name=chall.get("filename"),
                                url=self._client._get_api_url(
                                    f"challenges/{chall['id']}/download"
                                ),
                            )
                        ]
                        if chall.get("filename")
                        else []
                    ),
                    author=chall.get("creator"),
                    solved=chall.get("solved"),
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
        logger.debug("Submitting flag for challenge ID %s", challenge_id)

        try:
            resp = await self._client._http.post(
                self._client._get_api_url("flags/own"),
                json={"challenge_id": challenge_id, "flag": flag},
            )
            data = resp.json()
            message = data.get("message")
            return SubmissionResult(correct=(resp.status_code == 200), message=message)

        except BadRequestError as e:
            message = str(e)
            if "already owned" in message.lower():
                return SubmissionResult(correct=True, message=message)
            else:
                return SubmissionResult(correct=False, message=message)

        except Exception:
            logger.exception("Unexpected error during flag submission.")
            return SubmissionResult(
                correct=False, message="Submission failed due to an unexpected error."
            )

    async def _get_challenge_categories(self) -> Dict[int, str]:
        resp = await self._client._http.get(
            self._client._get_api_url("public/challenge-categories")
        )

        self._category_cache = {item["id"]: item["name"] for item in resp.json()}
        return self._category_cache

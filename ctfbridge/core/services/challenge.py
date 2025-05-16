from ctfbridge.base.services.challenge import ChallengeService
from ctfbridge.models.challenge import Challenge
from ctfbridge.parsers.enrich import enrich_challenge
from ctfbridge.exceptions import ChallengeFetchError
from typing import List


class CoreChallengeService(ChallengeService):
    def __init__(self, client):
        self._client = client

    @staticmethod
    def _filter_challenges(
        challenges,
        *,
        solved: bool | None = None,
        min_points: int | None = None,
        max_points: int | None = None,
        category: str | None = None,
        categories: list[str] | None = None,
        tags: list[str] | None = None,
        name_contains: str | None = None,
    ) -> List[Challenge]:
        result = challenges

        if solved is not None:
            result = [c for c in result if c.solved == solved]
        if min_points is not None:
            result = [c for c in result if c.value >= min_points]
        if max_points is not None:
            result = [c for c in result if c.value <= max_points]
        if category:
            result = [c for c in result if c.category == category]
        if categories:
            result = [c for c in result if c.category in categories]
        if tags:
            result = [
                c
                for c in result
                if all(tag in [t.name for t in c.tags] for tag in tags)
            ]
        if name_contains:
            lower_sub = name_contains.lower()
            result = [c for c in result if lower_sub in c.name.lower()]

        return result

    async def get_by_id(self, challenge_id: str, enrich: bool = True) -> Challenge:
        challenges = await self.get_all(enrich=False)
        for chall in challenges:
            if chall.id == challenge_id:
                if enrich:
                    chall = enrich_challenge(chall)
                return chall
        raise ChallengeFetchError(f"Challenge with id {challenge_id} not found.")

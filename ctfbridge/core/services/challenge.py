from typing import List

from ctfbridge.base.services.challenge import ChallengeService
from ctfbridge.exceptions import ChallengeFetchError
from ctfbridge.models.challenge import Challenge
from ctfbridge.models.filter import FilterOptions
from ctfbridge.parsers.enrich import enrich_challenge


class CoreChallengeService(ChallengeService):
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
        filters = FilterOptions(
            solved=solved,
            min_points=min_points,
            max_points=max_points,
            category=category,
            categories=categories,
            tags=tags,
            name_contains=name_contains,
            enrich=enrich,
        )

        base = await self._fetch_base_challenges()

        if self.base_has_details:
            if enrich:
                base = self._enrich(base)
            base = self._filter_challenges(base, filters)
            return base

        base = self._filter_challenges(base, filters)

        detailed = await self._fetch_details(base)

        if enrich:
            detailed = self._enrich(detailed)

        detailed = self._filter_challenges(detailed, filters)

        return detailed

    async def get_by_id(self, challenge_id: str, enrich: bool = True) -> Challenge:
        if self.base_has_details:
            all_challenges = await self.get_all(detailed=False, enrich=False)
            for chal in all_challenges:
                if chal.id == challenge_id:
                    return enrich_challenge(chal) if enrich else chal
            raise ChallengeFetchError(f"Challenge with ID '{challenge_id}' not found.")
        else:
            return await self._fetch_challenge_by_id(challenge_id, enrich=enrich)

    async def _fetch_challenge_by_id(self, challenge_id: str, enrich: bool = True) -> Challenge:
        raise NotImplementedError(
            "Platform must implement _fetch_challenge_by_id if base_has_details is False."
        )

    async def _fetch_details(self, base: List[Challenge]) -> List[Challenge]:
        challenges = [await self.get_by_id(chal.id, enrich=False) for chal in base]
        return challenges

    def _enrich(self, challenges: List[Challenge]) -> List[Challenge]:
        return [enrich_challenge(c) for c in challenges]

    def _filter_challenges(self, challenges, filters: FilterOptions) -> List[Challenge]:
        result = challenges
        if filters.solved is not None:
            result = [c for c in result if c.solved == filters.solved]
        if filters.min_points is not None:
            result = [c for c in result if c.value and c.value >= filters.min_points]
        if filters.max_points is not None:
            result = [c for c in result if c.value and c.value <= filters.max_points]
        if filters.category:
            result = [c for c in result if c.category == filters.category]
        if filters.categories:
            result = [c for c in result if c.category in filters.categories]
        if filters.tags:
            result = [
                c for c in result if all(t in [tag.value for tag in c.tags] for t in filters.tags)
            ]
        if filters.name_contains:
            lc = filters.name_contains.lower()
            result = [c for c in result if lc in c.name.lower()]
        return result

    @property
    def base_has_details(self) -> bool:
        return False

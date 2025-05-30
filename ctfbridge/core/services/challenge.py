import asyncio
from abc import abstractmethod
from typing import List

from ctfbridge.base.services.challenge import ChallengeService
from ctfbridge.exceptions import ChallengeFetchError
from ctfbridge.models.challenge import Challenge
from ctfbridge.models.filter import FilterOptions
from ctfbridge.processors.enrich import enrich_challenge


class CoreChallengeService(ChallengeService):
    """
    Core implementation of the challenge service.
    Provides common challenge fetching, filtering, and enrichment functionality.
    """

    @property
    def base_has_details(self) -> bool:
        """
        Whether the base challenge list includes full challenge details.
        If False, individual challenge details must be fetched separately.
        """
        return False

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
        )

        base = await self._fetch_challenges()

        if self.base_has_details:
            if enrich:
                base = self._enrich(base)
            base = self._filter_challenges(base, filters)
            return base

        base = self._filter_challenges(base, filters)

        detailed_challenges = await self._fetch_details(base)

        if enrich:
            detailed_challenges = self._enrich(detailed_challenges)

        detailed_challenges = self._filter_challenges(detailed_challenges, filters)

        return detailed_challenges

    async def get_by_id(self, challenge_id: str, enrich: bool = True) -> Challenge:
        if self.base_has_details:
            all_challenges = await self.get_all(detailed=False, enrich=False)
            for chal in all_challenges:
                if chal.id == challenge_id:
                    return enrich_challenge(chal) if enrich else chal
            raise ChallengeFetchError(f"Challenge with ID '{challenge_id}' not found.")
        else:
            return await self._fetch_challenge_by_id(challenge_id)

    async def _fetch_challenges(self) -> List[Challenge]:
        """
        Fetch the base list of challenges from the platform.
        Must be implemented by platform-specific services.

        Returns:
            List of basic challenge objects
        """
        pass

    async def _fetch_challenge_by_id(self, challenge_id: str) -> Challenge:
        """
        Fetch a specific challenge's details by ID.
        Must be implemented by platform-specific services if base_has_details is False.

        Args:
            challenge_id: The challenge ID to fetch

        Returns:
            The challenge object with full details

        Raises:
            NotImplementedError: If not implemented by the platform service
        """
        raise NotImplementedError(
            "Platform must implement _fetch_challenge_by_id if base_has_details is False."
        )

    async def _fetch_details(self, base: List[Challenge]) -> List[Challenge]:
        """
        Fetch full details for a list of basic challenge objects.

        Args:
            base: List of basic challenge objects

        Returns:
            List of challenges with full details
        """
        if not base:
            return []
        tasks = [self.get_by_id(chal.id, enrich=False) for chal in base]
        detailed_challenges = await asyncio.gather(*tasks)
        return [chal for chal in detailed_challenges if chal is not None]

    def _enrich(self, challenges: List[Challenge]) -> List[Challenge]:
        """
        Enrich challenges with additional metadata.

        Args:
            challenges: List of challenges to enrich

        Returns:
            List of enriched challenges
        """
        return [enrich_challenge(c) for c in challenges]

    def _filter_challenges(
        self, challenges: List[Challenge], filters: FilterOptions
    ) -> List[Challenge]:
        """
        Filter challenges based on the provided filter options.

        Args:
            challenges: List of challenges to filter
            filters: Filter criteria to apply

        Returns:
            List of challenges matching all filter criteria
        """
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

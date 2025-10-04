import asyncio
from abc import abstractmethod
from typing import Any, AsyncGenerator, List, Sequence

from ctfbridge.base.services.challenge import ChallengeService
from ctfbridge.exceptions import ChallengeFetchError
from ctfbridge.models.challenge import Challenge, FilterOptions
from ctfbridge.processors.enrich import enrich_challenge


def _match_value(actual, expected, *, strict: bool) -> bool:
    if expected is None:
        return True
    if actual is None:
        return not strict
    return actual == expected


def _match_min(actual, minimum, *, strict: bool) -> bool:
    if minimum is None:
        return True
    if actual is None:
        return not strict
    return actual >= minimum


def _match_max(actual, maximum, *, strict: bool) -> bool:
    if maximum is None:
        return True
    if actual is None:
        return not strict
    return actual <= maximum


def _match_subset(actual_set, expected_list, *, strict: bool) -> bool:
    if not expected_list:
        return True
    if not actual_set:
        return not strict
    return set(expected_list).issubset(actual_set)


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
        filters: FilterOptions | None = None,
        detailed: bool = True,
        enrich: bool = True,
        concurrency: int = -1,
        **kwargs: Any,
    ) -> List[Challenge]:
        return [
            c
            async for c in self.iter_all(
                detailed=detailed,
                enrich=enrich,
                concurrency=concurrency,
                filters=filters,
                **kwargs,
            )
        ]

    async def iter_all(
        self,
        *,
        filters: FilterOptions | None = None,
        detailed: bool = True,
        enrich: bool = True,
        concurrency: int = -1,
        **kwargs: Any,
    ) -> AsyncGenerator[Challenge, None]:
        if filters is None:
            filters = FilterOptions(**kwargs)

        base = await self._fetch_challenges()

        # -------------------------------------------------------------
        # Case 1 – Details already present or not requested
        # -------------------------------------------------------------
        if self.base_has_details or not detailed:
            for chal in base:
                if enrich:
                    chal = enrich_challenge(chal)
                if self._passes_filters(chal, filters, strict=True):
                    yield chal
            return

        # -------------------------------------------------------------
        # Case 2 – Details required → choose concurrency strategy
        # -------------------------------------------------------------

        async def fetch_detail(stub: Challenge) -> Challenge | None:
            detail = await self.get_by_id(stub.id, enrich=False)
            if enrich:
                detail = enrich_challenge(detail)
            return detail if self._passes_filters(detail, filters, strict=True) else None

        stubs: Sequence[Challenge] = [
            s for s in base if self._passes_filters(s, filters, strict=False)
        ]
        if not stubs:
            return

        # ------------------------ strategy ---------------------------
        if concurrency == 0:
            for stub in stubs:
                res = await fetch_detail(stub)
                if res:
                    yield res
            return

        async def run_tasks(max_workers: int | None):
            sem = asyncio.Semaphore(max_workers) if max_workers is not None else None

            async def limited(stub: Challenge):
                if sem:
                    async with sem:
                        return await fetch_detail(stub)
                return await fetch_detail(stub)

            tasks = [asyncio.create_task(limited(s)) for s in stubs]
            for coro in asyncio.as_completed(tasks):
                yield await coro

        async for item in run_tasks(None if concurrency < 0 else concurrency):
            yield item

    async def get_by_id(self, challenge_id: str, enrich: bool = True) -> Challenge:
        if self.base_has_details:
            all_challenges = await self.get_all(detailed=False, enrich=False)
            for chal in all_challenges:
                if chal.id == challenge_id:
                    return enrich_challenge(chal) if enrich else chal
            raise ChallengeFetchError(f"Challenge with ID '{challenge_id}' not found.")
        else:
            return await self._fetch_challenge_by_id(challenge_id)

    @abstractmethod
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

    def _passes_filters(self, chal: Challenge, filters: FilterOptions, *, strict: bool) -> bool:
        """
        Check whether a challenge satisfies every filter.

        Args:
            chal: The :class:`~ctfbridge.models.challenge.Challenge` under evaluation.
            filters: Filter criteria supplied by the caller.
            strict: ``False`` during the stub stage - missing fields count as
                match; ``True`` during the detail stage - missing values count
                as failures.

        Returns:
            bool: ``True`` if the challenge passes all filters under the
            given strictness level.
        """
        if not _match_value(chal.solved, filters.solved, strict=strict):
            return False
        if not _match_min(chal.value, filters.min_points, strict=strict):
            return False
        if not _match_max(chal.value, filters.max_points, strict=strict):
            return False
        if not _match_value(chal.category, filters.category, strict=strict):
            return False
        if filters.categories and (
            chal.category not in filters.categories if chal.category else strict
        ):
            return False
        if not _match_subset(set(chal.tags or []), filters.tags or [], strict=strict):
            return False

        # --- attachment / service flags ---------------------------------
        if filters.has_attachments is not None:
            if chal.has_attachments is None:
                if strict:
                    return False
            elif chal.has_attachments is not filters.has_attachments:
                return False
        if filters.has_services is not None:
            if chal.has_services is None:
                if strict:
                    return False
            elif chal.has_services is not filters.has_services:
                return False

        # --- name substring ---------------------------------------------
        if filters.name_contains:
            if chal.name is None:
                if strict:
                    return False
            elif filters.name_contains.lower() not in chal.name.lower():
                return False
        return True

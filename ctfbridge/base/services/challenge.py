from abc import ABC
from typing import List, Optional, AsyncGenerator

from ctfbridge.models import Challenge, SubmissionResult


class ChallengeService(ABC):
    async def get_all(
        self,
        *,
        detailed: bool = True,
        enrich: bool = True,
        concurrency: int = -1,
        solved: bool | None = None,
        min_points: int | None = None,
        max_points: int | None = None,
        category: str | None = None,
        categories: list[str] | None = None,
        tags: list[str] | None = None,
        name_contains: str | None = None,
    ) -> List[Challenge]:
        """
        Fetch all challenges.

        Args:
            detailed: If True, fetch full detail for each challenge using additional requests.
                      If False, return only the basic metadata from the listing endpoint.
                      Note: Setting this to False improves performance on platforms where
                      detailed challenge data requires per-challenge requests.
            enrich: If True, apply parsers to enrich the challenge (e.g., author, services).
            concurrency: -1 = unlimited, 0 = sequential, N > 0 = bounded to N workers.
            solved: If set, filter by solved status (True for solved, False for unsolved).
            min_points: If set, only include challenges worth at least this many points.
            max_points: If set, only include challenges worth at most this many points.
            category: If set, only include challenges in this category.
            categories: If set, only include challenges in one of these categories.
            tags: If set, only include challenges that have all of these tags.
            name_contains: If set, only include challenges whose name contains this substring (case-insensitive).

        Returns:
            List[Challenge]: A list of all challenges.

        Raises:
            ChallengeFetchError: If challenge listing fails.
            ChallengesUnavailableError: If the challenges are not available
            NotAuthenticatedError: If login is required.
            ServiceUnavailableError: If the server is down.
        """
        raise NotImplementedError

    async def iter_all(
        self,
        *,
        detailed: bool = True,
        enrich: bool = True,
        concurrency: int = -1,
        solved: bool | None = None,
        min_points: int | None = None,
        max_points: int | None = None,
        category: str | None = None,
        categories: list[str] | None = None,
        tags: list[str] | None = None,
        has_attachments: bool | None = None,
        has_services: bool | None = None,
        name_contains: str | None = None,
    ) -> AsyncGenerator[Challenge, None]:
        """
        Stream challenges lazily instead of returning a full list.

        Args:
            detailed: If True, fetch full detail for each challenge using additional requests.
                      If False, return only the basic metadata from the listing endpoint.
                      Note: Setting this to False improves performance on platforms where
                      detailed challenge data requires per-challenge requests.
            enrich: If True, apply parsers to enrich the challenge (e.g., author, services).
            concurrency: -1 = unlimited, 0 = sequential, N > 0 = bounded to N workers.
            solved: If set, filter by solved status (True for solved, False for unsolved).
            min_points: If set, only include challenges worth at least this many points.
            max_points: If set, only include challenges worth at most this many points.
            category: If set, only include challenges in this category.
            categories: If set, only include challenges in one of these categories.
            tags: If set, only include challenges that have all of these tags.
            name_contains: If set, only include challenges whose name contains this substring (case-insensitive).

        Yields:
            Challenge: Each challenge that matches all filter criteria.

        Raises:
            ChallengeFetchError: If challenge listing fails.
            ChallengesUnavailableError: If the challenges are not available
            NotAuthenticatedError: If login is required.
            ServiceUnavailableError: If the server is down.
        """
        raise NotImplementedError
        yield

    async def get_by_id(self, challenge_id: str, enrich: bool = True) -> Optional[Challenge]:
        """
        Fetch details for a specific challenge.

        Args:
            enrich: If True, apply parsers to enrich the challenge (e.g., author, services).
            challenge_id: The challenge ID.

        Returns:
            Challenge: The challenge details.

        Raises:
            ChallengeFetchError: If challenge cannot be loaded.
            ChallengeNotFoundError: If the challenge could not be found.
            NotAuthenticatedError: If login is required.
            ChallengesUnavailableError: If the challenges are not available
        """
        raise NotImplementedError

    async def submit(self, challenge_id: str, flag: str) -> SubmissionResult:
        """
        Submit a flag for a challenge.

        Args:
            challenge_id: The challenge ID.
            flag: The flag to submit.

        Returns:
            SubmissionResult: The result of the submission.

        Raises:
            SubmissionError: If the submission endpoint fails or returns an invalid response.
            ChallengeNotFoundError: If the challenge could not be found.
            NotAuthenticatedError: If the user is not logged in.
            CTFInactiveError: If the CTF is locked.
            RateLimitError: If submitting too quickly.
        """
        raise NotImplementedError

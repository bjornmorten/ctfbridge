from abc import ABC
from typing import Any, AsyncGenerator, List, Optional

from ctfbridge.models import Challenge, FilterOptions, SubmissionResult


class ChallengeService(ABC):
    async def get_all(
        self,
        *,
        filters: FilterOptions | None = None,
        detailed: bool = True,
        enrich: bool = True,
        concurrency: int = -1,
        **kwargs: Any,
    ) -> List[Challenge]:
        """
        Fetch all challenges.

        Args:
            filters: Structured filter options. If not provided,
                     individual filter fields can be passed as keyword arguments.
            detailed: If True, fetch full detail for each challenge using additional requests.
                      If False, return only the basic metadata from the listing endpoint.
                      Note: Setting this to False improves performance on platforms where
                      detailed challenge data requires per-challenge requests.
            enrich: If True, apply parsers to enrich the challenge (e.g., author, services).
            concurrency: -1 = unlimited, 0 = sequential, N > 0 = bounded to N workers.
            **kwargs: Alternative dynamic filters used only if `filters` is None.

        Returns:
            List[Challenge]: A list of all challenges.

        Raises:
            ChallengeFetchError: If challenge listing fails.
            ChallengesUnavailableError: If the challenges are not available
            NotAuthenticatedError: If login is required.
            NotAuthorizedError: If user don't have access.
            ServiceUnavailableError: If the server is down.
        """
        raise NotImplementedError

    async def iter_all(
        self,
        *,
        filters: FilterOptions | None = None,
        detailed: bool = True,
        enrich: bool = True,
        concurrency: int = -1,
        **kwargs: Any,
    ) -> AsyncGenerator[Challenge, None]:
        """
        Stream challenges lazily instead of returning a full list.

        Args:
            filters: Structured filter options. If not provided,
                     individual filter fields can be passed as keyword arguments.
            detailed: If True, fetch full detail for each challenge using additional requests.
                      If False, return only the basic metadata from the listing endpoint.
                      Note: Setting this to False improves performance on platforms where
                      detailed challenge data requires per-challenge requests.
            enrich: If True, apply parsers to enrich the challenge (e.g., author, services).
            concurrency: -1 = unlimited, 0 = sequential, N > 0 = bounded to N workers.
            **kwargs: Alternative dynamic filters used only if `filters` is None.

        Yields:
            Challenge: Each challenge that matches all filter criteria.

        Raises:
            ChallengeFetchError: If challenge listing fails.
            ChallengesUnavailableError: If the challenges are not available
            NotAuthenticatedError: If login is required.
            NotAuthorizedError: If user don't have access.
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
            NotAuthorizedError: If user don't have access.
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
            NotAuthorizedError: If user don't have access.
            CTFInactiveError: If the CTF is locked.
            RateLimitError: If submitting too quickly.
        """
        raise NotImplementedError

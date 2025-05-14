from abc import ABC
from typing import List, Optional

from ctfbridge.models import Challenge, SubmissionResult


class ChallengeService(ABC):
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
        """
        Fetch all challenges.

        Args:
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
            ChallengeFetchError: If challenge data cannot be fetched.
        """
        raise NotImplementedError

    async def get_by_id(self, challenge_id: str) -> Optional[Challenge]:
        """
        Fetch details for a specific challenge.

        Args:
            challenge_id: The challenge ID.

        Returns:
            Challenge: The challenge details.

        Raises:
            ChallengeFetchError: If challenge data cannot be fetched.
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
            SubmissionError: If submission fails or the response is invalid.
        """
        raise NotImplementedError

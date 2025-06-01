import logging
from typing import List

import httpx

from ctfbridge.core.services.scoreboard import CoreScoreboardService
from ctfbridge.exceptions import ScoreboardFetchError, NotAuthenticatedError
from ctfbridge.models.scoreboard import ScoreboardEntry as CoreScoreboardEntry

from ctfbridge.platforms.rctf.models.scoreboard import RCTFScoreboardResponse
from ctfbridge.platforms.rctf.http.endpoints import Endpoints

logger = logging.getLogger(__name__)


class RCTFScoreboardService(CoreScoreboardService):
    def __init__(self, client):
        self._client = client

    async def _fetch_scoreboard(self, limit: int) -> List[CoreScoreboardEntry]:
        """
        Fetches the scoreboard from rCTF with optional pagination.
        """
        results: List[CoreScoreboardEntry] = []
        offset = 0
        fetched_count = 0
        page_size = 100

        try:
            while True:
                # Cap how many we request in this round based on user-specified limit
                request_limit = min(page_size, limit - fetched_count) if limit > 0 else page_size
                if request_limit <= 0:
                    break

                logger.debug(f"Fetching scoreboard: offset={offset}, limit={request_limit}")
                response = await self._client.get(
                    Endpoints.Scoreboard.NOW,
                    params={"limit": request_limit, "offset": offset},
                )
                response.raise_for_status()

                # Parse and validate full response
                parsed = RCTFScoreboardResponse(**response.json())

                leaderboard_entries = parsed.data.leaderboard
                if not leaderboard_entries:
                    break  # No more data

                for i, entry in enumerate(leaderboard_entries):
                    try:
                        rank = offset + i + 1
                        results.append(entry.to_core_model(rank=rank))
                        fetched_count += 1
                    except Exception as e:
                        logger.error(f"Error parsing scoreboard entry {entry}: {e}")
                        continue

                    if limit > 0 and fetched_count >= limit:
                        break

                if len(leaderboard_entries) < request_limit:
                    break  # No more data available from API

                offset += len(leaderboard_entries)

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                logger.warning("Unauthorized when fetching rCTF scoreboard.")
                raise NotAuthenticatedError(
                    "Authentication may be required to fetch rCTF scoreboard."
                ) from e
            logger.error(f"HTTP error: {e}")
            raise ScoreboardFetchError(
                f"Failed to fetch scoreboard: {e.response.status_code}"
            ) from e
        except (ValueError, TypeError) as e:
            logger.error(f"Failed to parse rCTF scoreboard: {e}")
            raise ScoreboardFetchError("Invalid response format from rCTF server.") from e
        except Exception as e:
            logger.exception("Unexpected error during scoreboard fetch")
            raise ScoreboardFetchError(f"Unexpected error: {e}")

        return results

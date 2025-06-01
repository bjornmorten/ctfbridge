import logging
from typing import List

import httpx  # For error handling

from ctfbridge.core.services.scoreboard import CoreScoreboardService
from ctfbridge.exceptions import (
    ScoreboardFetchError,
    NotAuthenticatedError,
)  # Added NotAuthenticatedError
from ctfbridge.models.scoreboard import ScoreboardEntry as CoreScoreboardEntry

# Import new rCTF specific models and endpoints
from ctfbridge.platforms.rctf.models.scoreboard import (
    RCTFScoreboardEntryData,
)  # Assuming this model is defined
from ctfbridge.platforms.rctf.http.endpoints import Endpoints

logger = logging.getLogger(__name__)


class RCTFScoreboardService(CoreScoreboardService):
    def __init__(self, client):
        self._client = client

    async def _fetch_scoreboard(self, limit: int) -> List[CoreScoreboardEntry]:
        """
        Fetches the scoreboard from rCTF, handling pagination.
        This method is called by the CoreScoreboardService's get_top method.

        Args:
            limit: The maximum number of entries to return. If 0, fetches all entries.
        """
        scoreboard: List[CoreScoreboardEntry] = []
        offset = 0
        fetched_count = 0
        # rCTF typically uses a page size of 100 for its leaderboard
        # but this can be confirmed by observing API behavior or documentation.
        page_size = 100

        try:
            while True:
                # Determine how many entries to request in the current API call.
                # This is either page_size or less if the user's limit is being approached.
                request_limit = page_size
                if limit > 0:  # If a specific user limit is set
                    if fetched_count >= limit:
                        break  # Already fetched enough entries
                    request_limit = min(page_size, limit - fetched_count)

                # If the calculated request_limit is 0 or less due to user limit, stop.
                if limit > 0 and request_limit <= 0:
                    break

                api_params = {"limit": request_limit, "offset": offset}

                logger.debug(
                    f"Fetching rCTF scoreboard page: offset={offset}, limit={request_limit}"
                )
                response = await self._client.get(Endpoints.Scoreboard.NOW, params=api_params)
                response.raise_for_status()  # Check for HTTP errors

                data = response.json().get("data", {})
                partial_scoreboard_data = data.get("leaderboard", [])

                if not isinstance(partial_scoreboard_data, list):
                    logger.error(
                        f"Unexpected format for scoreboard data from rCTF: {partial_scoreboard_data}"
                    )
                    raise ScoreboardFetchError("Invalid scoreboard data format from rCTF.")

                if not partial_scoreboard_data:  # No more entries returned from the API
                    break

                for i, entry_data in enumerate(partial_scoreboard_data):
                    if not isinstance(entry_data, dict):
                        logger.warning(f"Skipping invalid scoreboard entry data item: {entry_data}")
                        continue
                    try:
                        rctf_entry = RCTFScoreboardEntryData(**entry_data)
                        # Calculate rank based on the overall position in the fetched list.
                        # rCTF might also provide a 'rank' field directly in entry_data.
                        # If so, prefer `entry_data.get('rank', offset + i + 1)`.
                        current_rank = offset + i + 1
                        scoreboard.append(rctf_entry.to_core_model(rank=current_rank))
                        fetched_count += 1
                    except Exception as e:  # Catch Pydantic validation error for individual entry
                        logger.error(
                            f"Failed to parse individual rCTF scoreboard entry ('{entry_data.get('name', 'N/A')}'): {e}"
                        )
                        # Optionally, skip this entry and continue

                    # If user-defined limit is reached, stop fetching more.
                    if limit > 0 and fetched_count >= limit:
                        break

                if (limit > 0 and fetched_count >= limit) or (
                    len(partial_scoreboard_data) < request_limit and limit == 0
                ):  # Fetched less than requested, implies end of data for "fetch all"
                    break

                offset += len(partial_scoreboard_data)

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:  # Unauthorized
                logger.warning(f"Unauthorized when fetching rCTF scoreboard: {e}")
                # Some rCTF instances might require auth for scoreboard
                raise NotAuthenticatedError(
                    "Authentication may be required to fetch rCTF scoreboard."
                ) from e
            logger.error(f"HTTP error fetching rCTF scoreboard: {e}")
            raise ScoreboardFetchError(
                f"Failed to fetch scoreboard from rCTF: {e.response.status_code}"
            ) from e
        except (
            ValueError,
            TypeError,
        ) as e:  # Handles JSON decoding errors or Pydantic validation errors
            logger.error(f"Error parsing rCTF scoreboard data: {e}")
            raise ScoreboardFetchError(
                "Invalid response format from rCTF server (scoreboard)."
            ) from e
        except Exception as e:  # Catch any other unexpected errors
            logger.exception("Unexpected error during rCTF scoreboard fetch")
            raise ScoreboardFetchError(f"An unexpected error occurred: {str(e)}")

        return scoreboard

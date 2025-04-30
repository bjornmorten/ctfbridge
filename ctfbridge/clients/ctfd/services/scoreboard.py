from typing import List

from ctfbridge.exceptions import ChallengeFetchError
from ctfbridge.models.scoreboard import ScoreboardEntry
from ctfbridge.services import ScoreboardService


class CTFdScoreboardService(ScoreboardService):
    """
    Base scoreboard service.
    """

    def __init__(self, client):
        super().__init__(client)

    def get_top(self, limit: int = 0) -> List[ScoreboardEntry]:
        """
        Return the top scoreboard entries.

        Args:
            limit: Optional limit of how many entries to return. 0 = all.
        """
        resp = self.client.session.get(
            f"{self.client.base_url}/api/v1/scoreboard",
        )

        try:
            data = resp.json()["data"]
        except Exception:
            raise ChallengeFetchError("Invalid response format from server (scoreboard).")

        scoreboard = []
        for entry in data:
            scoreboard.append(
                ScoreboardEntry(
                    name=entry.get("name", "unknown"),
                    score=entry.get("score", 0),
                    rank=entry.get("pos", 0)
                )
            )

        if limit:
            return scoreboard[:limit]
        else:
            return scoreboard

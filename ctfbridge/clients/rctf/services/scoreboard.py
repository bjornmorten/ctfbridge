from typing import List

from ctfbridge.exceptions import ChallengeFetchError
from ctfbridge.models.scoreboard import ScoreboardEntry
from ctfbridge.services import ScoreboardService


class RCTFScoreboardService(ScoreboardService):
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
        resp = self.client.session.get(f"{self.client.base_url}/api/v1/leaderboard/now?limit=0&offset=100")
        total = resp.json()["data"]["total"]

        if limit:
            limit = min(limit, total)
        else:
            limit = total

        scoreboard = []
        for offset in range(0, limit, 100):
            curr_limit = min(100, limit - offset)
            resp = self.client.session.get(f"{self.client.base_url}/api/v1/leaderboard/now?limit={curr_limit}&offset={offset}")

            partial_scoreboard = resp.json()["data"]["leaderboard"]
            for i, entry in enumerate(partial_scoreboard):
                scoreboard.append(ScoreboardEntry(
                    name=entry["name"],
                    score=entry["score"],
                    rank=offset + i + 1
                ))

        return scoreboard

from abc import ABC, abstractmethod
from typing import List

from ctfbridge.models.scoreboard import ScoreboardEntry
from ctfbridge.services import ScoreboardService


class DemoScoreboardService(ScoreboardService):
    """
    Base scoreboard service.
    """

    def __init__(self, client):
        super().__init__(client)

    def get_top(self, limit: int = 0) -> List[ScoreboardEntry]:
        scoreboard = [
            ScoreboardEntry(
                name="Iku-toppene",
                score=1337,
                rank=1
            ),
            ScoreboardEntry(
                name='Ekho',
                score=500,
                rank=2
            ),
            ScoreboardEntry(
                name='EPT',
                score=450,
                rank=3
            ),
            ScoreboardEntry(
                name='Coldboots',
                score=400,
                rank=4
            )
        ]

        if limit:
            return scoreboard[:limit]
        else:
            return scoreboard

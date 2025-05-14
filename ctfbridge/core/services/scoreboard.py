from ctfbridge.base.services.scoreboard import ScoreboardService


class CoreScoreboardService(ScoreboardService):
    def __init__(self, client):
        self._client = client

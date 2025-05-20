import logging
from typing import List

from ctfbridge.core.services.scoreboard import CoreScoreboardService
from ctfbridge.exceptions import ScoreboardFetchError
from ctfbridge.models.scoreboard import ScoreboardEntry

logger = logging.getLogger(__name__)


class BergScoreboardService(CoreScoreboardService):
    def __init__(self, client):
        self._client = client

from typing import List

from ctfbridge.exceptions import ScoreboardFetchError
from ctfbridge.core.services.scoreboard import CoreScoreboardService
from ctfbridge.models.scoreboard import ScoreboardEntry

import logging

logger = logging.getLogger(__name__)


class HTBScoreboardService(CoreScoreboardService):
    def __init__(self, client):
        self._client = client

from abc import ABC, abstractmethod
from ctfbridge.models.challenge import Challenge


class BaseChallengeParser(ABC):
    @abstractmethod
    def apply(self, challenge: Challenge) -> Challenge:
        pass

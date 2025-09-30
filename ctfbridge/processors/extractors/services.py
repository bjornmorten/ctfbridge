import logging
from ctfbridge.models.challenge import Challenge
from ctfbridge.processors.base import BaseChallengeParser
from ctfbridge.processors.helpers.services import extract_services_from_text
from ctfbridge.processors.registry import register_parser

logger = logging.getLogger(__name__)


@register_parser
class ServiceExtractor(BaseChallengeParser):
    """Extracts service information from challenge descriptions."""

    def can_handle(self, challenge: Challenge) -> bool:
        return not challenge.services and bool(challenge.description)

    def _process(self, challenge: Challenge) -> Challenge:
        try:
            services = extract_services_from_text(challenge.description)
            challenge.services.extend(services)
        except Exception as e:
            logger.error(f"Failed to extract service information: {e}")
        return challenge

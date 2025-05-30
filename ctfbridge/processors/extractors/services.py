import logging
import re
from typing import Optional, Tuple
from urllib.parse import urlparse

from ctfbridge.models.challenge import Challenge, Service, ServiceType
from ctfbridge.processors.base import BaseChallengeParser
from ctfbridge.processors.helpers.url_classifier import classify_links
from ctfbridge.processors.helpers.url_extraction import extract_links
from ctfbridge.processors.registry import register_parser

logger = logging.getLogger(__name__)

# Service-related regular expressions
NC_RE = re.compile(r"(?:nc|netcat)\s+(?:-[nv]+\s+)?(\S+)\s+(\d+)", re.IGNORECASE)
TELNET_RE = re.compile(r"telnet\s+(\S+)\s+(\d+)", re.IGNORECASE)
FTP_RE = re.compile(r"ftp\s+(\S+)(?:\s+(\d+))?", re.IGNORECASE)
SSH_RE = re.compile(r"ssh\s+(?:-p\s+(\d+)\s+)?(?:\S+@)?(\S+)", re.IGNORECASE)
# HTTP URLs
HTTP_RE = re.compile(r"https?://[^/\s:]+(?::(\d+))?", re.IGNORECASE)


@register_parser
class ServiceExtractor(BaseChallengeParser):
    """Extracts service information from challenge descriptions."""

    def can_handle(self, challenge: Challenge) -> bool:
        """Check if this parser should process the challenge.

        Returns True if has description.
        """
        return bool(challenge.description)

    def _process(self, challenge: Challenge) -> Challenge:
        """Extract service information from the challenge description.

        Args:
            challenge: The challenge to process.

        Returns:
            The challenge with extracted service information.
        """
        try:
            desc = challenge.description
            services = []

            # Try to match command-line service patterns
            for match in NC_RE.finditer(desc):
                services.append(
                    Service(
                        type=ServiceType.TCP,
                        host=match.group(1),
                        port=int(match.group(2)),
                        raw=match.group(0),
                    )
                )

            for match in TELNET_RE.finditer(desc):
                services.append(
                    Service(
                        type=ServiceType.TELNET,
                        host=match.group(1),
                        port=int(match.group(2)),
                        raw=match.group(0),
                    )
                )

            for match in FTP_RE.finditer(desc):
                if ":" not in match.group(1):  # Skip malformed matches
                    services.append(
                        Service(
                            type=ServiceType.FTP,
                            host=match.group(1),
                            port=int(match.group(2) or 21),
                            raw=match.group(0),
                        )
                    )

            for match in SSH_RE.finditer(desc):
                if match.group(2) and ":" not in match.group(2):  # Skip malformed matches
                    services.append(
                        Service(
                            type=ServiceType.SSH,
                            host=match.group(2),
                            port=int(match.group(1) or 22),
                            raw=match.group(0),
                        )
                    )

            # Try to find HTTP services from URLs
            for match in HTTP_RE.finditer(desc):
                url = match.group(0)
                host, port = self._get_host_port(url)
                services.append(
                    Service(
                        type=ServiceType.HTTP,
                        host=host,
                        port=port,
                        url=url,
                        raw=url,
                    )
                )

            # Remove duplicates while preserving order
            seen = set()
            unique_services = []
            for service in services:
                key = (service.type, service.host, service.port)
                if key not in seen:
                    seen.add(key)
                    unique_services.append(service)

            challenge.services = unique_services

        except Exception as e:
            logger.error(f"Failed to extract service information: {e}")

        return challenge

    @staticmethod
    def _get_host_port(url: str, default_scheme: str = "http") -> Tuple[str, int]:
        """Extract host and port from a URL.

        Args:
            url: The URL to parse.
            default_scheme: The default scheme to use if none is specified.

        Returns:
            A tuple of (host, port).

        Raises:
            ValueError: If the host cannot be parsed from the URL.
        """
        parsed = urlparse(url, scheme=default_scheme)
        host = parsed.hostname
        if host is None:
            raise ValueError(f"Could not parse host from {url!r}")

        port = parsed.port
        if port is None:
            port = 443 if parsed.scheme == "https" else 80
        return host, port

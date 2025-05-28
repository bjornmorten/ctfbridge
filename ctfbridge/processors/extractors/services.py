import re
from urllib.parse import urlparse

from ctfbridge.models.challenge import Challenge, Service, ServiceType
from ctfbridge.processors.base import BaseChallengeParser
from ctfbridge.processors.helpers.url_classifier import classify_links
from ctfbridge.processors.helpers.url_extraction import extract_links
from ctfbridge.processors.registry import register_parser

NC_RE = re.compile(r"nc\s+(\S+)\s+(\d+)", re.IGNORECASE)
TELNET_RE = re.compile(r"telnet\s+(\S+)\s+(\d+)", re.IGNORECASE)
FTP_RE = re.compile(r"ftp\s+(\S+)(?:\s+(\d+))?", re.IGNORECASE)
SSH_RE = re.compile(r"ssh\s+(?:\S+@)?(\S+)(?:\s+-p\s*(\d+))?", re.IGNORECASE)


@register_parser
class ServiceExtractor(BaseChallengeParser):
    def apply(self, challenge: Challenge) -> Challenge:
        if challenge.service or not challenge.description:
            return challenge

        desc = challenge.description

        if match := NC_RE.search(desc):
            challenge.service = Service(
                type=ServiceType.TCP,
                host=match.group(1),
                port=int(match.group(2)),
                raw=match.group(0),
            )
        elif match := TELNET_RE.search(desc):
            challenge.service = Service(
                type=ServiceType.TELNET,
                host=match.group(1),
                port=int(match.group(2)),
                raw=match.group(0),
            )
        elif match := FTP_RE.search(desc):
            challenge.service = Service(
                type=ServiceType.FTP,
                host=match.group(1),
                port=int(match.group(2) or 21),
                raw=match.group(0),
            )
        elif match := SSH_RE.search(desc):
            challenge.service = Service(
                type=ServiceType.SSH,
                host=match.group(1),
                port=int(match.group(2) or 22),
                raw=match.group(0),
            )
        else:
            urls = extract_links(challenge.description)
            urls = classify_links(urls)["services"]
            if urls:
                host, port = self._get_host_port(urls[0])
                challenge.service = Service(
                    type=ServiceType.HTTP,
                    host=host,
                    port=port,
                    url=urls[0],
                    raw=urls[0],
                )

        return challenge

    @staticmethod
    def _get_host_port(url: str, default_scheme: str = "http") -> tuple[str, int]:
        parsed = urlparse(url, scheme=default_scheme)
        host = parsed.hostname
        if host is None:
            raise ValueError(f"Could not parse host from {url!r}")

        port = parsed.port
        if port is None:
            port = 443 if parsed.scheme == "https" else 80
        return host, port

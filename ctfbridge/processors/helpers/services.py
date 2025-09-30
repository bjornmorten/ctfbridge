import re
from typing import List, Tuple
from urllib.parse import urlparse

from ctfbridge.models.challenge import Service, ServiceType
from ctfbridge.processors.helpers.url_classifier import classify_links

NC_RE = re.compile(r"(?:nc|netcat)\s+(?:-[nv]+\s+)?(\S+)\s+(\d+)", re.IGNORECASE)
TELNET_RE = re.compile(r"telnet\s+(\S+)\s+(\d+)", re.IGNORECASE)
FTP_RE = re.compile(r"ftp\s+(\S+)(?:\s+(\d+))?", re.IGNORECASE)
SSH_RE = re.compile(r"ssh\s+(?:-p\s+(\d+)\s+)?(?:\S+@)?(\S+)", re.IGNORECASE)
HTTP_RE = re.compile(r"https?://[^/\s:]+(?::(\d+))?", re.IGNORECASE)

HOSTPORT_PATH_RE = re.compile(
    r"(?:^|\s)((?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}|\d{1,3}(?:\.\d{1,3}){3}):(\d{1,5})(/\S*)?"
)


def _get_host_port(url: str, default_scheme: str = "http") -> Tuple[str, int]:
    parsed = urlparse(url, scheme=default_scheme)
    host = parsed.hostname
    if host is None:
        raise ValueError(f"Could not parse host from {url!r}")
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    return host, port


def extract_services_from_text(text: str) -> List[Service]:
    """Parse service connection info from arbitrary text."""
    services: List[Service] = []

    # nc / netcat
    for match in NC_RE.finditer(text):
        services.append(
            Service(
                type=ServiceType.TCP,
                host=match.group(1),
                port=int(match.group(2)),
                raw=match.group(0),
            )
        )

    # telnet
    for match in TELNET_RE.finditer(text):
        services.append(
            Service(
                type=ServiceType.TELNET,
                host=match.group(1),
                port=int(match.group(2)),
                raw=match.group(0),
            )
        )

    # ftp
    for match in FTP_RE.finditer(text):
        if ":" not in match.group(1):
            services.append(
                Service(
                    type=ServiceType.FTP,
                    host=match.group(1),
                    port=int(match.group(2) or 21),
                    raw=match.group(0),
                )
            )

    # ssh
    for match in SSH_RE.finditer(text):
        if match.group(2) and ":" not in match.group(2):
            services.append(
                Service(
                    type=ServiceType.SSH,
                    host=match.group(2),
                    port=int(match.group(1) or 22),
                    raw=match.group(0),
                )
            )

    # http(s) with explicit scheme
    http_matches = [url.group(0) for url in HTTP_RE.finditer(text)]
    http_services = classify_links(http_matches)["services"]
    for url in http_services:
        host, port = _get_host_port(url)
        services.append(
            Service(
                type=ServiceType.HTTP,
                host=host,
                port=port,
                url=url,
                raw=url,
            )
        )

    # host:port (with optional /path), no scheme
    for match in HOSTPORT_PATH_RE.finditer(text):
        host, port = match.group(1).strip(), int(match.group(2))
        path = match.group(3) or ""

        # classify as HTTP if there's a path
        if path:
            scheme = "https" if port == 443 else "http"
            url = f"{scheme}://{host}:{port}{path}"
            services.append(
                Service(
                    type=ServiceType.HTTP,
                    host=host,
                    port=port,
                    url=url,
                    raw=match.group(0),
                )
            )
        else:
            services.append(
                Service(
                    type=ServiceType.TCP,
                    host=host,
                    port=port,
                    raw=match.group(0),
                )
            )

    # Deduplicate (exact duplicates)
    seen = set()
    unique = []
    for s in services:
        key = (s.type, s.host, s.port)
        if key not in seen:
            seen.add(key)
            unique.append(s)

    # Drop generic TCP if a more specific service exists for the same host/port
    specific_types = {ServiceType.HTTP, ServiceType.FTP, ServiceType.SSH, ServiceType.TELNET}
    filtered = []
    for s in unique:
        if s.type == ServiceType.TCP and any(
            u.host == s.host and u.port == s.port and u.type in specific_types for u in unique
        ):
            continue
        filtered.append(s)

    return filtered

from urllib.parse import urlparse
from .utils import LinkClassifierContext
from .rules.file_extensions import is_filetype
from .rules.hostname import is_service_hostname
from .rules.port import has_explicit_port
from .rules.keyword import is_likely_service, is_likely_attachment
from .rules.path import is_root_path


def classify_links(links: list[str]) -> dict[str, list[str]]:
    attachments = []
    services = []

    for link in links:
        parsed = urlparse(link)
        if not parsed.scheme.startswith("http"):
            continue

        ctx = LinkClassifierContext(link=link, parsed=parsed)
        scores = {"attachment": 0, "service": 0}

        # Weighted scoring
        if is_filetype(ctx):
            scores["attachment"] += 3
        if is_likely_attachment(ctx):
            scores["attachment"] += 1

        if is_root_path(ctx):
            scores["service"] += 3
        if is_service_hostname(ctx):
            scores["service"] += 3
        if has_explicit_port(ctx):
            scores["service"] += 2
        if is_likely_service(ctx):
            scores["service"] += 1

        # Decide based on scores
        if scores["service"] > scores["attachment"]:
            services.append(link)
        else:
            attachments.append(link)

    return {
        "attachments": attachments,
        "services": services,
    }

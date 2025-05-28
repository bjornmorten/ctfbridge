from ..utils import LinkClassifierContext

SERVICE_KEYWORDS = ("run", "host", "port", "listen", "api", "docker", "service")
ATTACHMENT_KEYWORDS = ("file", "download", "resource", "attachment", "artifact")


def is_likely_service(ctx: LinkClassifierContext) -> bool:
    path = ctx.parsed.path.lower()
    netloc = ctx.parsed.netloc.lower()
    return any(kw in path or kw in netloc for kw in SERVICE_KEYWORDS)


def is_likely_attachment(ctx: LinkClassifierContext) -> bool:
    path = ctx.parsed.path.lower()
    netloc = ctx.parsed.netloc.lower()
    return any(kw in path or kw in netloc for kw in ATTACHMENT_KEYWORDS)

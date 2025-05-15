import re
from ..utils import LinkClassifierContext

PORT_PATTERN = re.compile(r"(?::|port=)(\d{2,5})")


def has_explicit_port(ctx: LinkClassifierContext) -> bool:
    return bool(ctx.parsed.port or PORT_PATTERN.search(ctx.link))

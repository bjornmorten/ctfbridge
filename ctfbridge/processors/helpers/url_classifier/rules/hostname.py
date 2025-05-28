from ..utils import LinkClassifierContext

SERVICE_HOSTNAMES = {"localhost", "127.0.0.1", "0.0.0.0", "::1", "internal", "service"}


def is_service_hostname(ctx: LinkClassifierContext) -> bool:
    return ctx.parsed.hostname in SERVICE_HOSTNAMES

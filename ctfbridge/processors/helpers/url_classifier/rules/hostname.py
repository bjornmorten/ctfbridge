import re
from typing import Set, Tuple

from ..utils import LinkClassifierContext

# Hostnames that typically indicate service endpoints
SERVICE_HOSTNAMES: Set[str] = {
    # Local development
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "::1",
    # Common service indicators
    "internal",
    "service",
    "services",
    # Common development environments
    "dev",
    "development",
    "staging",
    "prod",
    "production",
    # Load balancers and infrastructure
    "lb",
    "loadbalancer",
    "proxy",
    "gateway",
}

# Common service-related subdomains
SERVICE_SUBDOMAINS: Tuple[str, ...] = (
    "api",
    "app",
    "web",
    "admin",
    "portal",
    "dashboard",
    "auth",
    "login",
    "sso",
    "graphql",
    "ws",
    "socket",
    "monitor",
    "metrics",
    "status",
    "health",
)

# Cloud provider service domain patterns
CLOUD_DOMAINS: Tuple[str, ...] = (
    # Cloud platforms
    r"\.amazonaws\.com$",  # Only match the base domain
    r"\.herokuapp\.com$",
    r"\.azurewebsites\.net$",
    r"\.appspot\.com$",
    r"\.cloudfront\.net$",
    r"\.netlify\.app$",
    r"\.vercel\.app$",
    r"\.ngrok\.io$",
)

# Cloud storage domain patterns
STORAGE_DOMAINS: Tuple[str, ...] = (
    # AWS S3
    r"\.s3\.amazonaws\.com$",
    r"\.s3-[a-z0-9-]+\.amazonaws\.com$",
    # Azure Blob Storage
    r"\.blob\.core\.windows\.net$",
    # Google Cloud Storage
    r"\.storage\.googleapis\.com$",
    # Cloud storage services
    r"drive\.google\.com$",
    r"docs\.google\.com$",
    r"1drv\.ms$",
    r"onedrive\.live\.com$",
    r"\.sharepoint\.com$",
    r"\.dropboxusercontent\.com$",
    r"\.box\.com$",
)


def is_storage_hostname(ctx: LinkClassifierContext) -> bool:
    """Check if the URL hostname matches known storage service patterns.

    Args:
        ctx: The URL classification context.

    Returns:
        True if the hostname matches a known storage service pattern.
    """
    hostname = ctx.parsed.hostname.lower() if ctx.parsed.hostname else ""
    return any(re.search(pattern, hostname) for pattern in STORAGE_DOMAINS)


def is_service_hostname(ctx: LinkClassifierContext) -> bool:
    """Check if the URL hostname matches known service patterns.

    Checks for:
    - Known service hostnames
    - Common service subdomains
    - Cloud provider domains

    Args:
        ctx: The URL classification context.

    Returns:
        True if the hostname matches a known service pattern.
    """
    hostname = ctx.parsed.hostname.lower() if ctx.parsed.hostname else ""

    # Check exact hostname matches
    if any(part in SERVICE_HOSTNAMES for part in hostname.split(".")):
        return True

    # Check service subdomains
    if any(hostname.startswith(f"{sub}.") for sub in SERVICE_SUBDOMAINS):
        return True

    # Check cloud provider domains, but not if it's a storage domain
    if is_storage_hostname(ctx):
        return False

    return any(re.search(pattern, hostname) for pattern in CLOUD_DOMAINS)

import re
from typing import Tuple

from ..utils import LinkClassifierContext

# Version number pattern in paths
VERSION_PATTERN = re.compile(r"/v\d+(?:\.\d+)*(?:-\w+)?/?")

# Common paths that indicate service endpoints
SERVICE_PATHS: Tuple[str, ...] = (
    # API and service endpoints
    "/api",
    "/rest",
    "/graphql",
    "/grpc",
    "/soap",
    "/rpc",
    "/v1",
    "/v2",
    "/v3",
    "/api/v",
    "/rest/v",
    # Authentication and user management
    "/auth",
    "/login",
    "/oauth",
    "/sso",
    "/register",
    # Admin and monitoring
    "/admin",
    "/dashboard",
    "/metrics",
    "/health",
    "/status",
    "/monitor",
    "/prometheus",
    "/grafana",
    # WebSocket endpoints
    "/ws",
    "/websocket",
    "/socket",
    "/stream",
)

# Common paths that indicate file downloads
ATTACHMENT_PATHS: Tuple[str, ...] = (
    # Download directories
    "/files",
    "/downloads",
    "/attachments",
    "/artifacts",
    "/resources",
    "/assets",
    "/static",
    "/media",
    # Repository paths
    "/releases",
    "/dist",
    "/packages",
    "/binaries",
    "/repo",
    "/repository",
    "/archive",
    # Version indicators
    "/v1.0",
    "/v2.0",
    "/release-",
    "/version-",
    # Cloud storage paths
    "/download",
    "/view",
    "/file/d",  # Generic cloud storage
    "/uc",
    "/open",  # Google Drive
    "/download.aspx",
    "/download/",  # OneDrive/SharePoint
    "/s",
    "/dl",  # Dropbox
)

# Cloud storage URL patterns that indicate file downloads
CLOUD_STORAGE_PATTERNS: Tuple[str, ...] = (
    # Google Drive
    r"/file/d/[a-zA-Z0-9_-]+",  # Direct file links
    r"docs.google.com/[^/]+/d/[a-zA-Z0-9_-]+",  # Various Google Docs types
    # OneDrive
    r"1drv\.ms/[a-zA-Z0-9_-]+",  # Short links
    r"onedrive\.live\.com/.*redir.*",  # Redirect links
    # Dropbox
    r"dropbox\.com/s/[a-zA-Z0-9_-]+",  # Shared files
    # AWS S3
    r"s3\.amazonaws\.com/[^/]+/[^/]+",  # Direct bucket access
    r"s3-[a-z0-9-]+\.amazonaws\.com/[^/]+",  # Region-specific
)


def is_cloud_storage_download(ctx: LinkClassifierContext) -> bool:
    """Check if the URL matches cloud storage download patterns.

    Args:
        ctx: The URL classification context.

    Returns:
        True if the URL matches cloud storage download patterns.
    """
    return any(re.search(pattern, ctx.link.lower()) for pattern in CLOUD_STORAGE_PATTERNS)


def is_root_path(ctx: LinkClassifierContext) -> bool:
    """Check if the URL points to a root path.

    A root path is considered to be either "/" or "" with no additional
    parameters, query string, or fragment identifier.

    Args:
        ctx: The URL classification context.

    Returns:
        True if the URL points to a root path.
    """
    return (
        ctx.parsed.path in ["", "/"]
        and not ctx.parsed.params
        and not ctx.parsed.query
        and not ctx.parsed.fragment
    )


def is_service_path(ctx: LinkClassifierContext) -> bool:
    """Check if the URL path matches common service patterns.

    Args:
        ctx: The URL classification context.

    Returns:
        True if the path matches a service pattern.
    """
    path = ctx.parsed.path.lower()

    # Split path into segments and check each one
    segments = [s for s in path.split("/") if s]

    # First check if we're in a known attachment context
    for i, segment in enumerate(segments):
        if any(pattern.strip("/") == segment for pattern in ATTACHMENT_PATHS):
            # If we're in an attachment path, version numbers are likely release versions
            return False

    # Then check for service patterns
    for segment in segments:
        # Check if any segment matches a service pattern without the slashes
        if any(pattern.strip("/") == segment for pattern in SERVICE_PATHS):
            return True

    # Also check full path against patterns
    return any(pattern in path for pattern in SERVICE_PATHS)


def is_attachment_path(ctx: LinkClassifierContext) -> bool:
    """Check if the URL path matches common attachment/download patterns.

    Args:
        ctx: The URL classification context.

    Returns:
        True if the path matches an attachment pattern.
    """
    path = ctx.parsed.path.lower()

    # First check cloud storage patterns
    if is_cloud_storage_download(ctx):
        return True

    # Split path into segments and check each one
    segments = [s for s in path.split("/") if s]

    # First check for attachment path segments
    for segment in segments:
        if any(pattern.strip("/") == segment for pattern in ATTACHMENT_PATHS):
            return True

    # Check common download paths
    if any(pattern in path for pattern in ATTACHMENT_PATHS):
        return True

    # Check for version numbers in path, but only if we're not in a service context
    if VERSION_PATTERN.search(path):
        # Look at the path context to see if this is likely a release version
        for segment in segments:
            if any(pattern.strip("/") == segment for pattern in SERVICE_PATHS):
                return False  # Version number in service context (e.g. /api/v1)
        return True  # Version number in non-service context

    return False

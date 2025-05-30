from typing import Tuple

from ..utils import LinkClassifierContext

# Common file extensions that indicate downloadable content
FILE_EXTENSIONS: Tuple[str, ...] = (
    # Archives
    ".zip",
    ".tar",
    ".gz",
    ".bz2",
    ".xz",
    ".rar",
    ".7z",
    ".iso",
    ".img",
    ".dmg",
    # Documents
    ".txt",
    ".pdf",
    ".docx",
    ".xlsx",
    ".pptx",
    ".csv",
    ".md",
    ".rst",
    ".doc",
    ".xls",
    ".ppt",
    ".odt",
    ".pages",
    ".numbers",
    ".key",
    # Media
    ".png",
    ".jpg",
    ".jpeg",
    ".mp3",
    ".mp4",
    ".gif",
    ".svg",
    ".webp",
    ".wav",
    ".avi",
    ".mkv",
    ".mov",
    ".flac",
    ".m4a",
    # Binaries and Packages
    ".bin",
    ".exe",
    ".elf",
    ".so",
    ".dll",
    ".jar",
    ".war",
    ".apk",
    ".ipa",
    ".deb",
    ".rpm",
    ".msi",
    ".pkg",
    ".appimage",
    # Development
    ".py",
    ".js",
    ".cpp",
    ".c",
    ".h",
    ".java",
    ".go",
    ".rs",
    ".sh",
    ".pl",
    # Config and Data
    ".json",
    ".yaml",
    ".yml",
    ".xml",
    ".ini",
    ".conf",
    ".cfg",
    ".env",
    ".toml",
)


def is_filetype(ctx: LinkClassifierContext) -> bool:
    """Check if the URL points to a known file type.

    Args:
        ctx: The URL classification context.

    Returns:
        True if the URL path ends with a known file extension.
    """
    return any(ctx.parsed.path.lower().endswith(ext) for ext in FILE_EXTENSIONS)

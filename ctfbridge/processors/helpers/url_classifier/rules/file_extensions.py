from ..utils import LinkClassifierContext

FILE_EXTENSIONS = (
    ".zip",
    ".tar",
    ".gz",
    ".bz2",
    ".xz",
    ".rar",
    ".7z",
    ".txt",
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".mp3",
    ".mp4",
    ".docx",
    ".xlsx",
    ".pptx",
    ".csv",
    ".bin",
    ".exe",
    ".elf",
)


def is_filetype(ctx: LinkClassifierContext) -> bool:
    return any(ctx.parsed.path.lower().endswith(ext) for ext in FILE_EXTENSIONS)

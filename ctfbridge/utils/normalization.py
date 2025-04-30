CATEGORY_ALIASES = {
    # Reversing
    "reverse engineering": "rev",
    "reverse": "rev",
    "re": "rev",

    # Cryptography
    "cryptography": "crypto",
    "crypt": "crypto",

    # Web
    "web exploitation": "web",

    # Pwn
    "binary exploitation": "pwn",

    # Miscellaneous
    "miscellaneous": "misc",
    "other": "misc",
}


def normalize_category(name: str) -> str:
    """
    Normalize a CTF category name to a canonical lowercase value.

    Examples:
        "Rev" -> "reversing"
        "Crypto" -> "cryptography"
    """
    return CATEGORY_ALIASES.get(name.strip().lower(), name.strip().lower())

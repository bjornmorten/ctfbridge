import logging
from typing import Dict, List, Set

from ctfbridge.models.challenge import Challenge
from ctfbridge.processors.base import BaseChallengeParser
from ctfbridge.processors.registry import register_parser

logger = logging.getLogger(__name__)

# Core category definitions
CORE_CATEGORIES: Dict[str, Set[str]] = {
    # Reverse Engineering
    "rev": {
        "rev",
        "reverse",
        "reversing",
        "reverse engineering",
        "reverse-engineering",
        "decompile",
        "decompiling",
        "disassembly",
        "binary analysis",
        "malware",
        "malware analysis",
        "re",
        "crackme",
    },
    # Binary Exploitation
    "pwn": {
        "pwn",
        "pwning",
        "pwnable",
        "binary exploitation",
        "binary-exploitation",
        "binary",
        "exploit",
        "exploitation",
        "buffer overflow",
        "bof",
        "rop",
        "return oriented programming",
        "heap",
        "shellcode",
    },
    # Web Security
    "web": {
        "web",
        "web exploitation",
        "web-exploitation",
        "webapp",
        "web app",
        "web application",
        "web security",
        "websec",
        "xss",
        "sqli",
        "javascript",
        "php",
        "http",
        "csrf",
        "ssrf",
    },
    # Cryptography
    "crypto": {
        "crypto",
        "cryptography",
        "cryptographic",
        "encryption",
        "decryption",
        "cipher",
        "ciphers",
        "hash",
        "hashing",
        "rsa",
        "aes",
        "encoding",
        "classical crypto",
        "modern crypto",
    },
    # Forensics
    "forensics": {
        "forensics",
        "forensic",
        "digital forensics",
        "memory forensics",
        "disk forensics",
        "file forensics",
        "file analysis",
        "file carving",
        "memory dump",
        "disk image",
        "raw",
        "dump",
        "memdump",
        "autopsy",
        "sleuthkit",
        "encase",
        "ftk",
        "volatility",
    },
    # Network
    "network": {
        "network",
        "networking",
        "network security",
        "packet",
        "packets",
        "protocol",
        "protocols",
        "wireshark",
        "tcpdump",
        "traffic analysis",
        "network exploitation",
        "router",
        "switch",
        "firewall",
        "vpn",
        "dns",
        "dhcp",
        "network traffic",
        "network service",
    },
    # Steganography
    "stego": {
        "stego",
        "steganography",
        "steganographic",
        "image stego",
        "audio stego",
        "video stego",
        "stegano",
        "steganalysis",
    },
    # Miscellaneous
    "misc": {
        "misc",
        "miscellaneous",
        "random",
        "programming",
        "coding",
        "general skills",
        "general",
        "warmup",
        "sanity check",
        "scripting",
        "automation",
        "other",
    },
    # OSINT
    "osint": {
        "osint",
        "open source intelligence",
        "open-source intelligence",
        "recon",
        "reconnaissance",
        "information gathering",
        "social engineering",
        "doxing",
        "geolocation",
    },
    # Hardware
    "hardware": {
        "hardware",
        "iot",
        "internet of things",
        "embedded",
        "firmware",
        "arduino",
        "raspberry pi",
        "electronics",
        "circuit",
        "radio",
        "rf",
        "radio frequency",
        "sdr",
        "software defined radio",
    },
    # Mobile
    "mobile": {
        "mobile",
        "android",
        "ios",
        "iphone",
        "apk",
        "ipa",
        "mobile security",
        "mobile app",
        "mobile application",
        "smali",
        "dalvik",
    },
    # Cloud
    "cloud": {
        "cloud",
        "cloud security",
        "aws",
        "azure",
        "gcp",
        "cloud native",
        "kubernetes",
        "k8s",
        "docker",
        "container",
        "serverless",
        "infrastructure",
        "iac",
        "terraform",
    },
    # Blockchain
    "blockchain": {
        "blockchain",
        "smart contract",
        "smart contracts",
        "web3",
        "ethereum",
        "solidity",
        "defi",
        "nft",
        "cryptocurrency",
        "crypto currency",
        "bitcoin",
        "chain",
    },
    # Real World
    "realworld": {
        "realworld",
        "real world",
        "real-world",
        "realistic",
        "real life",
        "industry",
        "professional",
        "corporate",
    },
}

# Build reverse mapping for faster lookups
CATEGORY_MAP: Dict[str, str] = {
    variant: category for category, variants in CORE_CATEGORIES.items() for variant in variants
}

# Special case mappings for overlapping terms
SPECIAL_CASES = {
    "network forensics": "forensics",
    "packet forensics": "forensics",
    "pcap analysis": "network",
    "pcap": "network",
}


@register_parser
class CategoryNormalizer(BaseChallengeParser):
    """Normalizes challenge categories to a standard set."""

    def can_handle(self, challenge: Challenge) -> bool:
        """Check if this parser should process the challenge.

        Returns True if the challenge has categories to normalize.
        """
        return bool(challenge.categories)

    def _process(self, challenge: Challenge) -> Challenge:
        """Normalize the challenge categories.

        Args:
            challenge: The challenge to process.

        Returns:
            The challenge with normalized categories.
        """
        try:
            normalized = set()  # Use set to avoid duplicates
            for cat in challenge.categories:
                if cat is None:  # Handle None
                    normalized.add(None)
                    continue

                # Try exact match first
                raw = cat.strip().lower()

                # Check special cases first
                if raw in SPECIAL_CASES:
                    normalized.add(SPECIAL_CASES[raw])
                elif raw in CATEGORY_MAP:
                    normalized.add(CATEGORY_MAP[raw])
                else:
                    # Try partial matches
                    matches = set()
                    for variant in CATEGORY_MAP:
                        # Only match if the variant is a complete word in the category
                        # and not part of another word (e.g., "web" in "webinar")
                        words = raw.split()
                        if variant in words and not any(
                            w != variant and variant in w for w in words
                        ):
                            matches.add(CATEGORY_MAP[variant])

                    if len(matches) == 1:
                        # Single clear match
                        normalized.add(matches.pop())
                    elif not matches:
                        # No match found, keep original
                        normalized.add(raw)
                    # If multiple matches, skip ambiguous category and keep original
                    else:
                        normalized.add(raw)

            # If no categories were found, use original
            challenge.normalized_categories = sorted(cat for cat in normalized if cat is not None)
            if not challenge.normalized_categories and challenge.categories:
                challenge.normalized_categories = challenge.categories.copy()
        except Exception as e:
            logger.error(f"Failed to normalize categories: {e}")
            challenge.normalized_categories = challenge.categories.copy()

        return challenge

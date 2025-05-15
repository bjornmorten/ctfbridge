from ctfbridge.models.challenge import Challenge
from ctfbridge.parsers.base import BaseChallengeParser
from ctfbridge.parsers.registry import register_parser

CATEGORY_MAP = {
    "rev": "rev",
    "reverse engineering": "rev",
    "reversing": "rev",
    "reverse": "rev",
    "pwn": "pwn",
    "pwning": "pwn",
    "binary exploitation": "pwn",
    "binary": "pwn",
    "web": "web",
    "web exploitation": "web",
    "crypto": "crypto",
    "cryptography": "crypto",
    "forensics": "forensics",
    "forensic": "forensics",
    "misc": "misc",
    "miscellaneous": "misc",
    "random": "misc",
    "programming": "misc",
    "osint": "osint",
    "open source intelligence": "osint",
    "hardware": "hardware",
    "iot": "hardware",
    "firmware": "hardware",
    "mobile": "mobile",
    "android": "mobile",
    "ios": "mobile",
    "stego": "stego",
    "steganography": "stego",
    "network": "network",
    "cloud": "cloud",
    "blockchain": "blockchain",
    "smart contract": "blockchain",
    "smart contracts": "blockchain",
    "web3": "blockchain",
    "onsite": "onsite",
    "boot2root": "boot2root",
    "pentest": "pentest",
    "pentesting": "pentest",
    "penetration test": "pentest",
    "penetration testing": "pentest",
    "realworld": "realworld",
}


@register_parser
class CategoryNormalizer(BaseChallengeParser):
    def apply(self, challenge: Challenge) -> Challenge:
        normalized = []
        for cat in challenge.categories:
            raw = cat.strip().lower()
            normalized.append(CATEGORY_MAP.get(raw, raw))
        challenge.normalized_categories = normalized
        return challenge

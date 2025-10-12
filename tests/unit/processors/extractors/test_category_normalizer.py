import pytest

from ctfbridge.models.challenge import Challenge
from ctfbridge.processors.extractors.normalize_category import CategoryNormalizer


@pytest.fixture
def normalizer():
    return CategoryNormalizer()


@pytest.fixture
def basic_challenge():
    return Challenge(id="test", name="Test Challenge", description="", points=100, categories=[])


def test_can_handle(normalizer, basic_challenge):
    # Should not handle empty categories
    assert not normalizer.can_handle(basic_challenge)

    # Should handle if has categories
    basic_challenge.categories = ["test"]
    assert normalizer.can_handle(basic_challenge)


@pytest.mark.parametrize(
    "category",
    [
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
    ],
)
def test_normalize_rev_categories(normalizer, basic_challenge, category):
    basic_challenge.categories = [category]
    result = normalizer.apply(basic_challenge)
    assert result.normalized_categories == ["rev"]


@pytest.mark.parametrize(
    "category",
    [
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
    ],
)
def test_normalize_pwn_categories(normalizer, basic_challenge, category):
    basic_challenge.categories = [category]
    result = normalizer.apply(basic_challenge)
    assert result.normalized_categories == ["pwn"]


@pytest.mark.parametrize(
    "category",
    [
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
    ],
)
def test_normalize_web_categories(normalizer, basic_challenge, category):
    basic_challenge.categories = [category]
    result = normalizer.apply(basic_challenge)
    assert result.normalized_categories == ["web"]


@pytest.mark.parametrize(
    "category",
    [
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
    ],
)
def test_normalize_crypto_categories(normalizer, basic_challenge, category):
    basic_challenge.categories = [category]
    result = normalizer.apply(basic_challenge)
    assert result.normalized_categories == ["crypto"]


@pytest.mark.parametrize(
    "category",
    [
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
        "network forensics",
        "packet forensics",
    ],
)
def test_normalize_forensics_categories(normalizer, basic_challenge, category):
    basic_challenge.categories = [category]
    result = normalizer.apply(basic_challenge)
    assert result.normalized_categories == ["forensics"]


@pytest.mark.parametrize(
    "category",
    [
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
    ],
)
def test_normalize_misc_categories(normalizer, basic_challenge, category):
    basic_challenge.categories = [category]
    result = normalizer.apply(basic_challenge)
    assert result.normalized_categories == ["misc"]


@pytest.mark.parametrize(
    "category",
    [
        "osint",
        "open source intelligence",
        "open-source intelligence",
        "recon",
        "reconnaissance",
        "information gathering",
        "social engineering",
        "doxing",
        "geolocation",
    ],
)
def test_normalize_osint_categories(normalizer, basic_challenge, category):
    basic_challenge.categories = [category]
    result = normalizer.apply(basic_challenge)
    assert result.normalized_categories == ["osint"]


@pytest.mark.parametrize(
    "category",
    [
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
    ],
)
def test_normalize_hardware_categories(normalizer, basic_challenge, category):
    basic_challenge.categories = [category]
    result = normalizer.apply(basic_challenge)
    assert result.normalized_categories == ["hardware"]


@pytest.mark.parametrize(
    "category",
    [
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
    ],
)
def test_normalize_mobile_categories(normalizer, basic_challenge, category):
    basic_challenge.categories = [category]
    result = normalizer.apply(basic_challenge)
    assert result.normalized_categories == ["mobile"]


@pytest.mark.parametrize(
    "category",
    [
        "stego",
        "steganography",
        "steganographic",
        "image stego",
        "audio stego",
        "video stego",
    ],
)
def test_normalize_stego_categories(normalizer, basic_challenge, category):
    basic_challenge.categories = [category]
    result = normalizer.apply(basic_challenge)
    assert result.normalized_categories == ["stego"]


@pytest.mark.parametrize(
    "category",
    [
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
        "pcap",
        "pcap analysis",
    ],
)
def test_normalize_network_categories(normalizer, basic_challenge, category):
    basic_challenge.categories = [category]
    result = normalizer.apply(basic_challenge)
    assert result.normalized_categories == ["network"]


@pytest.mark.parametrize(
    "category",
    [
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
    ],
)
def test_normalize_cloud_categories(normalizer, basic_challenge, category):
    basic_challenge.categories = [category]
    result = normalizer.apply(basic_challenge)
    assert result.normalized_categories == ["cloud"]


@pytest.mark.parametrize(
    "category",
    [
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
    ],
)
def test_normalize_blockchain_categories(normalizer, basic_challenge, category):
    basic_challenge.categories = [category]
    result = normalizer.apply(basic_challenge)
    assert result.normalized_categories == ["blockchain"]


@pytest.mark.parametrize(
    "categories,expected",
    [
        (["web", "crypto", "pwn"], ["crypto", "pwn", "web"]),
        (["web", "web exploitation", "crypto"], ["crypto", "web"]),
    ],
)
def test_normalize_multiple_categories(normalizer, basic_challenge, categories, expected):
    basic_challenge.categories = categories
    result = normalizer.apply(basic_challenge)
    assert sorted(result.normalized_categories) == expected


@pytest.mark.parametrize(
    "categories,expected",
    [
        (["unknown", "custom"], ["custom", "unknown"]),
        (["web", "unknown", "crypto"], ["crypto", "unknown", "web"]),
    ],
)
def test_handle_unknown_categories(normalizer, basic_challenge, categories, expected):
    basic_challenge.categories = categories
    result = normalizer.apply(basic_challenge)
    assert sorted(result.normalized_categories) == expected


@pytest.mark.parametrize(
    "category,expected",
    [
        ("advanced web hacking", ["web"]),
        ("crypto-web", ["crypto-web"]),  # Ambiguous - keep original
    ],
)
def test_handle_partial_matches(normalizer, basic_challenge, category, expected):
    basic_challenge.categories = [category]
    result = normalizer.apply(basic_challenge)
    assert result.normalized_categories == expected


@pytest.mark.parametrize(
    "category", ["WEB", "Web", "web", "CRYPTO", "Crypto", "crypto", "PWN", "Pwn", "pwn"]
)
def test_handle_case_sensitivity(normalizer, basic_challenge, category):
    basic_challenge.categories = [category]
    result = normalizer.apply(basic_challenge)
    assert len(result.normalized_categories) == 1
    assert result.normalized_categories[0] == category.lower()

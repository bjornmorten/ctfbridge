import json
import time
from pathlib import Path

import pytest

from ctfbridge.utils import platform_cache


def test_set_and_get_valid_cache(tmp_path):
    # Patch the cache path
    platform_cache.CACHE_PATH = tmp_path / "cache.json"

    platform_cache.set_cached_platform("https://example.com", "ctfd", "https://example.com")
    result = platform_cache.get_cached_platform("https://example.com")

    assert result == ("ctfd", "https://example.com")


def test_expired_entry_returns_none(tmp_path):
    platform_cache.CACHE_PATH = tmp_path / "cache.json"
    old_timestamp = time.time() - (platform_cache.CACHE_TTL_SECONDS + 10)

    with open(platform_cache.CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump({"https://expired.com": ["ctfd", "https://expired.com", old_timestamp]}, f)

    result = platform_cache.get_cached_platform("https://expired.com")
    assert result is None


def test_corrupt_cache_file(tmp_path):
    platform_cache.CACHE_PATH = tmp_path / "corrupt.json"
    platform_cache.CACHE_PATH.write_text("{not: valid json}")

    result = platform_cache.load_platform_cache()
    assert result == {}


def test_entry_is_tuple(tmp_path):
    platform_cache.CACHE_PATH = tmp_path / "tuple_test.json"
    platform_cache.set_cached_platform("https://tuple.com", "ctfd", "https://tuple.com")

    result = platform_cache.load_platform_cache()
    assert isinstance(result["https://tuple.com"], tuple)

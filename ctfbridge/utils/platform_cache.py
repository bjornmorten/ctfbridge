import json
from pathlib import Path

CACHE_PATH = Path.home() / ".ctfbridge_platform_cache.json"


def load_platform_cache():
    if not CACHE_PATH.exists():
        return {}
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_platform_cache(cache: dict):
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


def get_cached_platform(url: str) -> tuple[str, str] | None:
    cache = load_platform_cache()
    return cache.get(url)


def set_cached_platform(url: str, platform: str, base_url: str):
    cache = load_platform_cache()
    cache[url] = (platform, base_url)
    save_platform_cache(cache)

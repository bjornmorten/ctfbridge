import asyncio
import ssl
import time
from typing import Tuple
from urllib.parse import urlparse, urlunparse
import logging

import httpx

from ctfbridge.exceptions import UnknownBaseURLError, UnknownPlatformError
from ctfbridge.platforms.registry import get_identifier_classes

logger = logging.getLogger(__name__)

_MAX_CONCURRENT_PROBES = 4
_FAILED_CANDIDATE_TTL = 300.0  # seconds
_failed_candidate_cache: dict[str, float] = {}


def _extract_ssl_error(exc: BaseException) -> ssl.SSLError | None:
    """
    Walk the chained exceptions to locate an SSL error, if any.
    """
    seen: set[int] = set()
    current: BaseException | None = exc

    while current and id(current) not in seen:
        if isinstance(current, ssl.SSLError):
            return current
        seen.add(id(current))
        current = getattr(current, "__cause__", None) or getattr(current, "__context__", None)

    return None


def _is_ssl_verification_disabled(http: httpx.AsyncClient) -> bool:
    """
    Best-effort check to see if SSL verification is disabled on the provided client.
    """
    explicit_setting = getattr(http, "_ctfbridge_verify_ssl", None)
    if explicit_setting is not None:
        return explicit_setting is False

    transport = getattr(http, "_transport", None)
    pool = getattr(transport, "_pool", None)
    ssl_context = getattr(pool, "_ssl_context", None)

    if ssl_context:
        return ssl_context.verify_mode == ssl.CERT_NONE

    return False


def _record_failure(candidate: str) -> None:
    _failed_candidate_cache[candidate] = time.monotonic()


def _is_recent_failure(candidate: str) -> bool:
    timestamp = _failed_candidate_cache.get(candidate)
    if timestamp is None:
        return False

    if time.monotonic() - timestamp > _FAILED_CANDIDATE_TTL:
        _failed_candidate_cache.pop(candidate, None)
        return False

    return True


def _clear_failure(candidate: str) -> None:
    _failed_candidate_cache.pop(candidate, None)


def _normalize_base_url(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return url
    return urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc,
            parsed.path.rstrip("/"),
            "",
            "",
            "",
        )
    )


def generate_candidate_base_urls(full_url: str) -> list[str]:
    parsed = urlparse(full_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {full_url}")

    scheme = parsed.scheme.lower()
    parts = parsed.path.strip("/").split("/") if parsed.path.strip("/") else []
    seen: set[str] = set()
    candidates: list[str] = []

    def _add(candidate: str) -> None:
        normalized = _normalize_base_url(candidate)
        if normalized not in seen:
            seen.add(normalized)
            candidates.append(normalized)

    for i in range(len(parts), -1, -1):
        path = "/" + "/".join(parts[:i]) if i > 0 else ""
        candidate = urlunparse((scheme, parsed.netloc, path.rstrip("/"), "", "", ""))
        _add(candidate)

    return candidates


def _expand_input_urls(input_url: str) -> list[str]:
    parsed = urlparse(input_url)
    if parsed.scheme and parsed.netloc:
        return [input_url]

    fallback = urlparse(f"//{input_url}")
    if not fallback.netloc:
        raise ValueError(f"Invalid URL: {input_url}")

    variants = []
    for scheme in ("https", "http"):
        variants.append(urlunparse((scheme, fallback.netloc, fallback.path, "", "", "")))
    return variants


async def _probe_candidates(
    http: httpx.AsyncClient,
    candidates: list[str],
) -> dict[str, tuple[httpx.Response | None, httpx.HTTPError | None]]:
    """
    Probe candidate URLs concurrently to reduce total detection time.
    """
    semaphore = asyncio.Semaphore(_MAX_CONCURRENT_PROBES)
    results: dict[str, tuple[httpx.Response | None, httpx.HTTPError | None]] = {}

    async def _fetch(candidate: str) -> None:
        async with semaphore:
            try:
                response = await http.get(candidate, timeout=5)
                results[candidate] = (response, None)
            except httpx.HTTPError as exc:
                results[candidate] = (None, exc)

    await asyncio.gather(*[asyncio.create_task(_fetch(candidate)) for candidate in candidates])
    return results


async def detect_platform(input_url: str, http: httpx.AsyncClient) -> Tuple[str, str]:
    """
    Detect the platform type and base URL from a possibly nested URL.

    Args:
        input_url: Domain or URL to the platform (scheme optional).
        http: A shared HTTP client.

    Returns:
        Platform name and platform base URL

    Raises:
        UnknownPlatformError: If no known platform is matched.
        UnknownBaseURL: If the platform is matched but no working base URL is found.
    """

    def _append_unique(items: list[str], value: str | None) -> None:
        if value and value not in items:
            items.append(value)

    identifier_classes = list(get_identifier_classes())
    raw_inputs = _expand_input_urls(input_url)
    ssl_verification_disabled = _is_ssl_verification_disabled(http)

    seen_candidates: set[str] = set()
    candidates: list[str] = []
    for raw_input in raw_inputs:
        for candidate in generate_candidate_base_urls(raw_input):
            if candidate not in seen_candidates:
                seen_candidates.add(candidate)
                candidates.append(candidate)

    parsed_candidates = {candidate: urlparse(candidate) for candidate in candidates}

    identifier_instances = [
        (name, IdentifierClass(http)) for name, IdentifierClass in identifier_classes
    ]
    pattern_names = {
        name
        for name, identifier in identifier_instances
        for parsed_candidate in parsed_candidates.values()
        if identifier.match_url_pattern(parsed_candidate)
    }
    ordered_identifiers = [
        *[(name, identifier) for name, identifier in identifier_instances if name in pattern_names],
        *[
            (name, identifier)
            for name, identifier in identifier_instances
            if name not in pattern_names
        ],
    ]

    failed_candidates: set[str] = set()
    reachable_candidates: list[str] = []

    async def _find_valid_base_url(
        identifier,
        preferred_candidates: list[str] | None = None,
    ):
        ordered_candidates: list[str] = []
        seen: set[str] = set()

        for candidate in preferred_candidates or []:
            if candidate not in seen:
                ordered_candidates.append(candidate)
                seen.add(candidate)

        for candidate in candidates:
            if candidate not in seen:
                ordered_candidates.append(candidate)
                seen.add(candidate)

        checked: set[str] = set()

        for base_candidate in ordered_candidates:
            try:
                canonical_candidate = identifier.get_base_url(base_candidate)
            except Exception as e:
                logger.exception(f"Failed to get base URL for {base_candidate}: {e}")
                canonical_candidate = None

            if canonical_candidate:
                return canonical_candidate

            if base_candidate in checked:
                continue
            checked.add(base_candidate)

            if base_candidate in failed_candidates:
                continue

            if await identifier.is_base_url(base_candidate):
                return base_candidate

            failed_candidates.add(base_candidate)

        raise UnknownBaseURLError(input_url)

    probe_targets = [candidate for candidate in candidates if not _is_recent_failure(candidate)]
    for skipped in candidates:
        if skipped not in probe_targets:
            failed_candidates.add(skipped)

    probe_results = await _probe_candidates(http, probe_targets) if probe_targets else {}

    # Step 1: Try static detection for each candidate while tracking reachability
    for candidate in candidates:
        response, error = probe_results.get(candidate, (None, None))

        if response is None:
            failed_candidates.add(candidate)
            if candidate in probe_results:
                _record_failure(candidate)
                ssl_error = _extract_ssl_error(error) if error else None
                if ssl_error:
                    if ssl_verification_disabled:
                        continue
                    detail = getattr(ssl_error, "reason", None) or str(ssl_error)
                    raise UnknownPlatformError(
                        f"SSL error while connecting to {candidate}: {detail}. "
                        "If this is expected, rerun with SSL verification disabled."
                    ) from error
            continue

        _clear_failure(candidate)

        final_candidate = _normalize_base_url(str(response.url))
        preferred_candidates: list[str] = []
        if final_candidate and final_candidate != candidate:
            preferred_candidates.append(final_candidate)
        preferred_candidates.append(candidate)

        for base in preferred_candidates:
            _clear_failure(base)
            _append_unique(reachable_candidates, base)

        for name, identifier in identifier_instances:
            detection = await identifier.static_detect(response)
            if detection:
                base_url = await _find_valid_base_url(identifier, preferred_candidates)
                return name, base_url

    if not reachable_candidates:
        raise UnknownPlatformError(f"Could not connect to {input_url}")

    # Step 2: Fallback to dynamic detection for reachable candidates
    for candidate in reachable_candidates:
        for name, identifier in ordered_identifiers:
            if await identifier.dynamic_detect(candidate):
                base_url = await _find_valid_base_url(identifier, [candidate])
                return name, base_url

    raise UnknownPlatformError(f"Could not detect platform from {input_url}")

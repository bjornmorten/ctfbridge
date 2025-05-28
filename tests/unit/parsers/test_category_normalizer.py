from ctfbridge.processors.extractors.normalize_category import CategoryNormalizer


def test_normalizes_category_to_rev(base_challenge):
    chal = base_challenge(categories=["reverse engineering"])
    result = CategoryNormalizer().apply(chal)
    assert result.normalized_category == "rev"


def test_preserves_original_category(base_challenge):
    chal = base_challenge(categories=["pwning"])
    result = CategoryNormalizer().apply(chal)
    assert result.category == "pwning"
    assert result.normalized_category == "pwn"


def test_perserves_unknown_category(base_challenge):
    chal = base_challenge(categories=["unknown"])
    result = CategoryNormalizer().apply(chal)
    assert result.normalized_category == "unknown"


def test_empty_category_list(base_challenge):
    chal = base_challenge(categories=[])
    result = CategoryNormalizer().apply(chal)
    assert result.normalized_categories == []


def test_mixed_known_and_unknown(base_challenge):
    chal = base_challenge(categories=["pwn", "reverse engineering", "alien"])
    result = CategoryNormalizer().apply(chal)
    assert result.normalized_categories == ["pwn", "rev", "alien"]

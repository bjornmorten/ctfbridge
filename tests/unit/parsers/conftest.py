import pytest

from ctfbridge.models.challenge import Challenge


@pytest.fixture
def base_challenge():
    return lambda **kwargs: Challenge(
        id=kwargs.get("id", "1"),
        name=kwargs.get("name", "test"),
        categories=kwargs.get("categories", ["misc"]),
        value=kwargs.get("value", 100),
        description=kwargs.get("description", ""),
        author=kwargs.get("author", None),
        tags=[],
        attachments=[],
    )

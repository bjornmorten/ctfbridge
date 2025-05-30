from urllib.parse import unquote, urlparse

from ctfbridge.models.challenge import Attachment, Challenge


def parse_ctfd_challenge(data: dict) -> Challenge:
    attachments = [
        Attachment(
            name=unquote(urlparse(url).path.split("/")[-1]),
            url=url,
        )
        for url in data.get("files", [])
    ]

    return Challenge(  # type: ignore[call-arg]
        id=str(data["id"]),
        name=data["name"],
        categories=[data["category"]] if data.get("category") else [],
        value=data.get("value"),
        description=data.get("description"),
        attachments=attachments,
        solved=data.get("solved_by_me", False),
    )

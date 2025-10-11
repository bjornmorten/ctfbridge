from bs4 import BeautifulSoup
import re
from ctfbridge.models.challenge import (
    Challenge,
    Attachment,
    Service,
    ServiceType,
    DownloadInfo,
    DownloadType,
    AttachmentCollection,
)


def parse_challenges(html: str) -> list[Challenge]:
    soup = BeautifulSoup(html, "html.parser")

    challenges = []
    current_category = None

    id_pattern = re.compile(r"onLayer\((\d+)\)")

    section = soup.select_one("section.color-1")
    if not section:
        return challenges

    for elem in section.contents:
        if elem.name == "br":
            continue

        if isinstance(elem, str):
            text = elem.strip()
            if text.startswith("[") and text.endswith("]"):
                current_category = text.strip("[]")
            continue

        if elem.name == "figure":
            caption = elem.find("figcaption")
            img_tag = elem.find("img")

            if not (caption and img_tag):
                continue

            onclick = img_tag.get("onclick", "")
            match = id_pattern.search(onclick)
            if not match:
                continue

            challenge_id = match.group(1)
            name = caption.text.strip()

            challenge = Challenge(
                id=challenge_id,
                name=name,
                categories=[current_category],
            )

            challenges.append(challenge)

    return challenges


def parse_challenge_detail(challenge: Challenge, html: str) -> Challenge:
    soup = BeautifulSoup(html, "html.parser")

    value = None
    value_tag = soup.find("a", href=re.compile(r"/writeup\.php"))
    if value_tag and "[" in value_tag.text:
        match = re.search(r"\[(\d+)\s*points?\]", value_tag.text)
        if match:
            value = int(match.group(1))

    textarea = soup.find("textarea")
    description = textarea.get_text(strip=False).strip() if textarea else None

    services = []
    attachments = []

    if description:
        bin_url_matches = re.findall(
            r"https?://pwnable\.kr/bin/[^\s'\"<>]+",
            description,
        )

        if bin_url_matches:
            for url in bin_url_matches:
                url = url.replace("http://", "https://")
                name = url.split("/bin/")[-1]
                attachments.append(
                    Attachment(
                        name=name,
                        download_info=DownloadInfo(
                            type=DownloadType.HTTP,
                            url=url,
                        ),
                    )
                )

        ssh_match = re.search(
            r"ssh\s+([^\s@]+)@([\w\.\-]+)\s+-p(\d+)(?:.*?\(pw:\s*([^)]+)\))?", description
        )
        if ssh_match:
            user, host, port, password = ssh_match.groups()
            services.append(
                Service(
                    host=host,
                    port=int(port),
                    type=ServiceType.SSH,
                    username=user,
                    password=password.strip() if password else None,
                    raw=ssh_match.group(0),
                )
            )

            if not attachments:
                if password and password.strip() == "guest":
                    attachments.append(
                        Attachment(
                            name=None,
                            download_info=DownloadInfo(
                                type=DownloadType.SSH,
                                host=host,
                                port=int(port),
                                username=user,
                                password=password.strip(),
                                path=f"/home/{user}/",
                            ),
                        )
                    )

    challenge.description = description
    challenge.services = services
    challenge.attachments = AttachmentCollection(attachments=attachments)
    challenge.value = value
    return challenge

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

    for a_tag in soup.select("a[data-toggle='modal'][data-target^='#chalModal']"):
        data_target = a_tag.get("data-target")
        if not data_target:
            continue

        modal_id = data_target.lstrip("#")
        modal = soup.select_one(f"div.modal#{modal_id}")
        if not modal:
            continue

        header = modal.select_one(".card-header.d-flex")
        if not header:
            continue

        name = header.select_one("div").get_text(strip=True)
        score = header.select_one(".ml-auto").get_text(strip=True)
        try:
            value = int(score)
        except ValueError:
            value = None

        author_div = modal.select_one(".card-header div:-soup-contains('Author:')")
        author = author_div.select_one("a").get_text(strip=True)

        desc_div = modal.select_one(".card-body")
        description = desc_div.get_text(strip=True) if desc_div else ""

        services = []
        svc_div = modal.select_one(".card-header div:-soup-contains('svc.pwnable.xyz')")
        if not svc_div:
            svc_text = None
            for d in modal.select(".card-header div"):
                text = d.get_text(strip=True)
                if "svc.pwnable.xyz" in text:
                    svc_text = text
                    break
        else:
            svc_text = svc_div.get_text(strip=True)

        if svc_text:
            m = re.search(r"([\w\.\-]+)\s*:\s*(\d+)", svc_text)
            if m:
                host, port = m.groups()
                services.append(
                    Service(type=ServiceType.TCP, host=host, port=int(port), raw=svc_text)
                )

        attachments = []
        for a in modal.select("a[href]"):
            href = a["href"]
            if href.startswith("/redisfiles/challenge_"):
                name_part = href.split("/")[-1]
                attachments.append(
                    Attachment(
                        name=name_part, download_info=DownloadInfo(type=DownloadType.HTTP, url=href)
                    )
                )

        challenges.append(
            Challenge(
                id=modal_id.replace("chalModal", ""),
                name=name,
                value=value,
                description=description,
                attachments=AttachmentCollection(attachments=attachments),
                services=services,
                categories=["pwn"],
                authors=[author],
            )
        )

    return challenges

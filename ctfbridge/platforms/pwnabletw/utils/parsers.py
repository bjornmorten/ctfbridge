from bs4 import BeautifulSoup
import re
from ctfbridge.models.challenge import Challenge, Attachment, Service, ServiceType


def parse_challenges(html: str) -> list[Challenge]:
    soup = BeautifulSoup(html, "html.parser")
    challenges = []

    for li in soup.select("li.challenge-entry"):
        challenge_id = li.get("id", "").replace("challenge-id-", "")

        name_tag = li.select_one(".tititle")
        name = name_tag.get_text(strip=True) if name_tag else None

        score_tag = li.select_one(".score i")
        value = None
        if score_tag and (m := re.search(r"(\d+)", score_tag.text)):
            value = int(m.group(1))

        desc_div = li.select_one(".description")

        attachments = []
        if desc_div:
            for a in desc_div.select("a[href]"):
                href = a["href"]
                if href.startswith("/static/chall") or href.startswith("/static/libc"):
                    name_part = href.split("/")[-1]
                    attachments.append(Attachment(name=name_part, url=href))

        services = []
        if desc_div:
            for code in desc_div.find_all("code"):
                code_text = code.get_text(strip=True)
                if not code_text.startswith("nc"):
                    continue

                parts = code_text.split()
                host = parts[1]
                port = int(parts[2])
                services.append(
                    Service(
                        type=ServiceType.TCP,
                        host=host,
                        port=port,
                        raw=code_text,
                    )
                )

        description = clean_description(desc_div)

        challenges.append(
            Challenge(
                id=challenge_id,
                name=name,
                value=value,
                description=description,
                attachments=attachments,
                services=services,
                categories=["pwn"],
            )
        )

    return challenges


def clean_description(desc_div) -> str:
    for a in desc_div.select("a[href]"):
        href = a["href"]
        if href.startswith("/static/chall") or href.startswith("/static/libc"):
            a.decompose()

    for code in desc_div.find_all("code"):
        code_text = code.get_text(strip=True)
        if code_text.startswith("nc "):
            code.decompose()

    for a in desc_div.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        a.replace_with(f"[{text}]({href})")

    for code in desc_div.find_all("code"):
        code.replace_with(f"`{code.get_text(strip=True)}`")

    for br in desc_div.find_all("br"):
        br.replace_with("\n\n")

    paragraphs = []
    for p in desc_div.find_all("p"):
        text = p.get_text(" ", strip=True)
        if text:
            text = text.strip().strip(":")
            text = text.replace(" .", ".")
            text = text.replace(" ,", ",")
            text = text.replace(" !", "!")
            paragraphs.append(text)

    text = "\n\n".join(paragraphs)

    return text

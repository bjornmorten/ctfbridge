from bs4 import BeautifulSoup
from typing import List
from ctfbridge.platforms.cryptohack.models.challenge import (
    CryptoHackCategory,
    CryptoHackChallenge,
    CryptoHackAttachment,
)
from ctfbridge.models.challenge import Service, ServiceType
import re


def parse_categories(html: str) -> List[CryptoHackCategory]:
    soup = BeautifulSoup(html, "html.parser")
    categories: List[CryptoHackCategory] = []

    for a_tag in soup.select("ul.listCards a[href^='/challenges/']"):
        h4_tag = a_tag.select_one("h4")
        if not h4_tag:
            continue

        name = h4_tag.get_text(strip=True)
        path = a_tag.get("href", "").strip()

        categories.append(CryptoHackCategory(name=name, path=path))

    return categories


def parse_challenges(html: str) -> List[CryptoHackChallenge]:
    soup = BeautifulSoup(html, "html.parser")
    challenges: List[CryptoHackChallenge] = []

    category_title = soup.select_one(".categoryTitle").text

    for subcategory in soup.select(".stage"):
        subcategory_title = subcategory.select_one("h4").text
        for challenge in subcategory.select("li.challenge"):
            id = challenge.select_one("li.challenge div.collapsible-header")["data-challenge"]
            name = challenge.select_one(".challenge-text").text

            solved = "You have solved this challenge" in challenge.text

            points_match = re.search(r"\b(\d+)\spts\b", challenge.text)
            if points_match:
                points = int(points_match.group(1))
            else:
                points = 0

            flag_format = None
            for label in soup.find_all("label"):
                text = label.get_text(strip=True)
                if "Enter flag here" in text:
                    match = re.search(r"([A-Za-z0-9_-]+\{[^}]*\})", text)
                    if match:
                        flag_format = match.group(1)

            desc_tag = challenge.select_one(".challengeDescription")
            description = desc_tag.get_text(separator="\n", strip=True) if desc_tag else ""

            authors = [
                a.get_text(strip=True)
                for a in challenge.select(".challengeDescription a.gold-link")
            ]

            files = []
            for a in challenge.select(".challengeDescription a[download]"):
                files.append(CryptoHackAttachment(name=a.get_text(strip=True), path=a["href"]))

            service = extract_service(desc_tag)

            cleaned_description = re.split(
                r"(Challenge contributed by|Play at|Connect at)", description
            )[0].strip()

            challenge = CryptoHackChallenge(
                id=id,
                name=name,
                category=category_title,
                subcategory=subcategory_title,
                description=cleaned_description,
                authors=authors,
                attachments=files,
                service=service,
                points=points,
                flag_format=flag_format,
                solved=solved,
            )

            challenges.append(challenge)

    return challenges


def extract_service(soup) -> Service | None:
    code = soup.find("code")
    if code and "Connect at" in soup.get_text():
        raw_text = code.get_text(strip=True)
        match = re.match(r"([a-zA-Z0-9\.\-_]+)\s+(\d+)", raw_text)
        if match:
            host, port = match.groups()
            return Service(
                type=ServiceType.TCP,
                host=host,
                port=int(port),
                raw=raw_text,
            )

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        target = a.get("target", "").lower()

        if "cryptohack.org" in href and target == "_blank":
            return Service(
                type=ServiceType.HTTP,
                port=443,
                url=href,
                raw=href,
            )

    return None

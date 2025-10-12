from bs4 import BeautifulSoup
import re

from ..models.models import Dojo, DojoSection, Module, Challenge


def parse_dojos_list(html: str) -> list[DojoSection]:
    """
    Parse the main /dojos page into structured sections of dojos.

    Returns a list of DojoSection objects, each containing Dojo entries.
    """
    soup = BeautifulSoup(html, "html.parser")
    sections: list[DojoSection] = []

    # Find all h2 tags that start a section
    for h2 in soup.find_all("h2"):
        section_title = h2.get_text(strip=True)

        ul = h2.find_next("ul", class_="card-list")
        if not ul:
            continue

        dojos: list[Dojo] = []

        for a_tag in ul.find_all("a", class_="text-decoration-none"):
            href = a_tag.get("href")
            slug = href.split("/")[-1] if href else None

            card = a_tag.find("li", class_="card")
            if not card:
                continue

            title_tag = card.find("h4", class_="card-title")
            title = title_tag.get_text(strip=True) if title_tag else "Unknown"

            dojos.append(
                Dojo(
                    title=title,
                    slug=slug,
                )
            )

        sections.append(
            DojoSection(
                title=section_title,
                dojos=dojos,
            )
        )

    return sections


def parse_dojo_detail(html: str) -> Dojo:
    """
    Parse a single dojo page (e.g. /dojo/intro-to-cybersecurity)
    into a Dojo object with a list of Modules.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Extract dojo title
    title_tag = soup.find("h1", class_="brand-mono-bold")
    title = title_tag.get_text(strip=True).replace(".", "") if title_tag else "Unknown Dojo"

    # Extract dojo slug from JS init variable or URL
    script_tag = soup.find("script", string=lambda s: s and "var init" in s)
    slug = None
    if script_tag and "dojo" in script_tag.text:
        import re

        match = re.search(r"'dojo':\s*\"([^\"]+)\"", script_tag.text)
        if match:
            slug = match.group(1)
    if not slug:
        # fallback: infer from <a href="/dojo/...">
        link = soup.find("a", href=lambda h: h and "/dojo/" in h)
        if link:
            slug = link["href"].split("/")[-1]

    # Extract modules
    modules = []
    modules_ul = soup.find("ul", class_="card-list")
    if modules_ul:
        for a_tag in modules_ul.find_all("a", class_="text-decoration-none"):
            href = a_tag.get("href", "").strip("/")
            module_slug = href.split("/")[-1] if "/" in href else href

            card = a_tag.find("li", class_="card")
            if not card:
                continue

            title_tag = card.find("h4", class_="card-title")
            module_title = title_tag.get_text(strip=True) if title_tag else "Unknown Module"

            modules.append(Module(title=module_title, slug=module_slug, challenges=[]))

    return Dojo(title=title, slug=slug, modules=modules)


def parse_module_detail(html: str):
    soup = BeautifulSoup(html, "html.parser")

    h1 = soup.find("h1", class_="brand-mono-bold")
    module_title = h1.get_text(strip=True).replace(".", "") if h1 else "Unknown Module"

    dojo_el = soup.select_one("h2.module-dojo a")
    dojo_title = dojo_el.get_text(strip=True).replace(".", "") if dojo_el else None

    module_slug = None
    script_tag = soup.find("script", string=lambda s: s and "var init" in s)
    if script_tag:
        match = re.search(r"'module':\s*\"([^\"]+)\"", script_tag.text)
        if match:
            module_slug = match.group(1)

    dojo_slug = None
    script_tag = soup.find("script", string=lambda s: s and "var init" in s)
    if script_tag:
        match = re.search(r"'dojo':\s*\"([^\"]+)\"", script_tag.text)
        if match:
            dojo_slug = match.group(1)

    # --- Challenges ---
    challenges = []
    for challenge_div in soup.select("div.accordion-item"):
        header = challenge_div.select_one("h4.challenge-name")
        if not header:
            continue

        title = header.get("data-challenge-name", header.get_text(strip=True))
        category = None  # TODO: parse

        # The description is in the next .challenge-description div
        desc_div = challenge_div.select_one("div.challenge-description")
        challenge_id = challenge_div.select_one("#challenge-id").get("value")
        challenge_slug = challenge_div.select_one("#challenge").get("value")
        description = desc_div.get_text("\n", strip=True) if desc_div else ""

        challenges.append(
            Challenge(
                id=challenge_id,
                slug=challenge_slug,
                title=title,
                category=category,
                description=description,
                dojo_title=dojo_title,
                module_title=module_title,
                dojo_slug=dojo_slug,
                module_slug=module_slug,
            )
        )

    return Module(
        title=module_title,
        slug=module_slug,
        challenges=challenges,
    )

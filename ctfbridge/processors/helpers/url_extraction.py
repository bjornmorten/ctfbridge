import re

# Match markdown-style links: [text](http://example.com)
MARKDOWN_LINK_RE = re.compile(r"\[.*?\]\((https?://[^\s)]+)\)", re.IGNORECASE)

# Match bare URLs: http(s)://...
BARE_URL_RE = re.compile(r"\bhttps?://[^\s)\"'<>]+", re.IGNORECASE)

# Match HTML <a href="..."> links
HTML_HREF_RE = re.compile(r'<a\s[^>]*href=["\'](https?://[^"\']+)["\']', re.IGNORECASE)


def extract_links(text: str) -> list[str]:
    links = set()

    links.update(MARKDOWN_LINK_RE.findall(text))
    links.update(BARE_URL_RE.findall(text))
    links.update(HTML_HREF_RE.findall(text))

    return sorted(links)

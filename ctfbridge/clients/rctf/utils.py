from urllib.parse import parse_qs, unquote, urlparse


def extract_token_from_url(url: str) -> str:
    """Extract team token from team invite URL."""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    extracted_token_list = query_params.get("token")
    if not extracted_token_list:
        raise ValueError("Invalid token URL: no token parameter found.")
    token = extracted_token_list[0]
    return token

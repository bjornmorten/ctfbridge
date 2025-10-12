import httpx
import base64
import json


async def get_csrf_token(session: httpx.Client) -> str | None:
    session_cookie = session.cookies.get("session")

    if not session_cookie:
        await session.get("https://cryptohack.org")
        session_cookie = session.cookies.get("session")
        if not session_cookie:
            return None

    try:
        jwt_parts = session_cookie.split(".")
        if len(jwt_parts) != 3:
            return None

        header_b64 = jwt_parts[0]
        padding = "=" * (-len(header_b64) % 4)
        header_json = base64.urlsafe_b64decode(header_b64 + padding)
        header_data = json.loads(header_json)

        return header_data.get("_csrf_token")

    except (ValueError, json.JSONDecodeError, IndexError):
        return None

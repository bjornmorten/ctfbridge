import asyncio

from ctfbridge import create_client
from ctfbridge.exceptions import UnknownBaseURLError, UnknownPlatformError


async def main():
    # Explicitly specify the platform and URL
    # This is useful if to reduce time spent identifying the platform.
    try:
        client = await create_client("https://demo.ctfd.io", platform="ctfd")
        print(
            f"Successfully created client for: {client.platform_url} (Platform: {client.platform_name})"
        )

        # Example of a potentially incorrect platform specification
        # client_rctf = await create_client("https://demo.ctfd.io", platform="rctf")
        # print(f"Client: {client_rctf.platform_url} (Platform: {client_rctf.platform_name})")

    except UnknownPlatformError as e:
        print(f"Error: {e}")
    except UnknownBaseURLError as e:
        print(f"Error: Could not determine base URL for {e.url}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())

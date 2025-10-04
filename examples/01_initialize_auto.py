import asyncio

from ctfbridge import create_client


async def main():
    # Auto-detects the platform (e.g., CTFd, rCTF) from the URL
    client = await create_client("https://demo.ctfd.io")
    print(
        f"Successfully created client for: {client.platform_url} (Platform: {client.platform_name})"
    )

    # You can now use the client to interact with the platform
    # e.g., await client.auth.login(...)
    #       challenges = await client.challenges.get_all()


if __name__ == "__main__":
    asyncio.run(main())

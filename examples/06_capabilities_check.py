import asyncio

from ctfbridge import create_client
from ctfbridge.exceptions import CTFBridgeError


async def main():
    """
    This example demonstrates how to check the capabilities of a platform
    before attempting to use a feature. This allows you to write scripts
    that can adapt to different CTF platforms gracefully.
    """
    # Using CTFd, which supports all features
    client = await create_client("https://demo.ctfd.io")
    print(f"Client for {client.platform_name} at {client.platform_url} created.")

    print("\n--- Checking Platform Capabilities ---")

    # Check for login support (synchronous property access)
    if client.capabilities.login:
        print("✅ This platform supports login.")
        try:
            # Example of adapting behavior based on capability
            await client.auth.login(username="user", password="password")
            print("   -> Login successful!")
        except CTFBridgeError as e:
            print(f"   -> Login failed: {e}")
    else:
        print("❌ This platform does not support login via ctfbridge.")

    # Check for flag submission support
    if client.capabilities.submit_flags:
        print("✅ This platform supports flag submission.")
    else:
        print("❌ This platform does not support flag submission.")

    # Check for scoreboard support
    if client.capabilities.view_scoreboard:
        print("✅ This platform supports viewing the scoreboard.")
        try:
            top_entry = await client.scoreboard.get_top(1)
            if top_entry:
                print(f"   -> Top rank: {top_entry[0].name} with {top_entry[0].score} points.")
        except CTFBridgeError as e:
            print(f"   -> Could not fetch scoreboard: {e}")
    else:
        print("❌ This platform does not support viewing the scoreboard.")


if __name__ == "__main__":
    asyncio.run(main())

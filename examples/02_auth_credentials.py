import asyncio

from ctfbridge import create_client
from ctfbridge.exceptions import CTFBridgeError, LoginError


async def main():
    # Initialize client (CTFd in this example)
    client = await create_client("https://demo.ctfd.io")

    try:
        # Attempt to login with username and password
        await client.auth.login(username="user", password="passworda")
        print("Login successful!")

    except LoginError as e:
        print(f"Login failed: {e}")
    except CTFBridgeError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())

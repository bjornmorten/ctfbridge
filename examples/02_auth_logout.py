import asyncio

from ctfbridge import create_client
from ctfbridge.exceptions import CTFBridgeError, LoginError


async def main():
    client = await create_client("https://demo.ctfd.io")

    try:
        try:
            await client.auth.login(username="user", password="password")
            print("Login successful (or seemed to be).")
        except LoginError:
            print("Login failed.")

        await client.auth.logout()
        print("Logout successful! Session cookies and auth headers are cleared.")

    except CTFBridgeError as e:
        print(f"A CTFBridge error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())

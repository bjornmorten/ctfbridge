import asyncio
from ctfbridge import create_client
from ctfbridge.exceptions import CTFBridgeError, UnauthorizedError


async def main():
    # Initialize client (works with CTFd, rCTF, HTB etc.)
    client = await create_client("https://demo.ctfd.io")
    # Authenticate to the platform
    await client.auth.login(username="user", password="password")  # Or token

    try:
        print("Fetching all challenges (basic details)...")
        # detailed=False fetches only basic info, usually faster.
        # enrich=False skips client-side enrichment
        # (parsing authors, attachments, services from description).
        challenges_basic = await client.challenges.get_all(detailed=False, enrich=False)
        if challenges_basic:
            print(f"Found {len(challenges_basic)} challenges (basic details):")
            for chal in challenges_basic[:3]:  # Print first 3
                print(
                    f"  ID: {chal.id}, Name: {chal.name}, Category: {chal.category}, Points: {chal.value}, Solved: {chal.solved}"
                )
        else:
            print("No challenges found or platform requires authentication.")

        print("\nFetching all challenges (detailed and enriched)...")
        # detailed=True fetches full details (might involve more requests per challenge on some platforms).
        # enrich=True applies client-side parsers to extract more info from descriptions.
        challenges_detailed = await client.challenges.get_all(detailed=True, enrich=True)
        if challenges_detailed:
            print(f"Found {len(challenges_detailed)} challenges (detailed):")
            for chal in challenges_detailed[:3]:  # Print first 3
                print(f"  ID: {chal.id}, Name: {chal.name}")
                print(f"    Category: {chal.category} (Normalized: {chal.normalized_category})")
                print(f"    Points: {chal.value}, Solved: {chal.solved}")
                print(f"    Description: {chal.description[:20]}...")
                print(f"    Authors: {chal.authors}")
                if chal.attachments:
                    print(f"    Attachments: {[att.name for att in chal.attachments]}")
        else:
            print("No challenges found.")

    except UnauthorizedError:
        print("Error: This operation requires authentication. Please login first.")
    except CTFBridgeError as e:
        print(f"A CTFBridge error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())

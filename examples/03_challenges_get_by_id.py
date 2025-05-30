import asyncio
from ctfbridge import create_client
from ctfbridge.exceptions import CTFBridgeError, ChallengeFetchError, UnauthorizedError


async def main():
    client = await create_client("https://demo.ctfd.io")
    await client.auth.login(username="user", password="password")

    # --- Get a known challenge ID from the platform ---
    # First, let's get all challenges to find a valid ID to query
    challenge_id_to_fetch = None
    try:
        print("Fetching a list of challenges to get a valid ID...")
        all_challenges = await client.challenges.get_all(detailed=False)
        if all_challenges:
            challenge_id_to_fetch = all_challenges[0].id  # Get the ID of the first challenge
            print(f"Will attempt to fetch details for challenge ID: {challenge_id_to_fetch}")
        else:
            print(
                "No challenges found to get an ID from. Make sure the platform is accessible and has challenges."
            )
            return
    except CTFBridgeError as e:
        print(f"Error fetching initial challenge list: {e}")
        return
    # --- End of getting a challenge ID ---

    if not challenge_id_to_fetch:
        print("Could not obtain a challenge ID to fetch.")
        return

    try:
        print(f"\nFetching challenge by ID: {challenge_id_to_fetch} (enriched)...")
        # enrich=True (default) applies client-side parsers
        challenge = await client.challenges.get_by_id(challenge_id_to_fetch)

        if challenge:
            print(f"Successfully fetched challenge: {challenge.name}")
            print(f"  ID: {challenge.id}")
            print(f"  Category: {challenge.category} (Normalized: {challenge.normalized_category})")
            print(f"  Points: {challenge.value}")
            print(f"  Solved: {challenge.solved}")
            print(f"  Description: {challenge.description[:200]}...")
            print(f"  Authors: {challenge.authors}")
            if challenge.attachments:
                print("  Attachments:")
                for att in challenge.attachments:
                    print(f"    - Name: {att.name}, URL: {att.url}")
        else:
            print(f"Challenge with ID {challenge_id_to_fetch} not found.")

    except ChallengeFetchError as e:
        print(f"Error fetching challenge by ID: {e}")
    except UnauthorizedError:
        print("Error: This operation requires authentication. Please login first.")
    except CTFBridgeError as e:
        print(f"A CTFBridge error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())

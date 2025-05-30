import asyncio
from ctfbridge import create_client
from ctfbridge.exceptions import (
    CTFBridgeError,
    ScoreboardFetchError,
    UnauthorizedError,
    CTFInactiveError,
)


async def main():
    # Using demo.ctfd.io, which usually has a public scoreboard
    client = await create_client("https://demo.ctfd.io")
    # For platforms requiring auth to see scoreboard, login first:
    # await client.auth.login(username="user", password="password")

    try:
        print("Fetching top 10 scoreboard entries...")
        # limit=0 would fetch all entries (if supported and not too large)
        top_10_entries = await client.scoreboard.get_top(limit=10)

        if top_10_entries:
            print("\n--- Top 10 Scoreboard ---")
            for entry in top_10_entries:
                print(f"  Rank: {entry.rank}, Name: {entry.name}, Score: {entry.score}")
        else:
            print("Scoreboard is empty or could not be fetched.")

        # Example: Fetching all scoreboard entries
        # print("\nFetching all scoreboard entries (limit=0)...")
        # all_entries = await client.scoreboard.get_top(limit=0)
        # if all_entries:
        #     print(f"Total entries on scoreboard: {len(all_entries)}")
        #     print(f"Top entry: Rank {all_entries[0].rank}, Name: {all_entries[0].name}, Score: {all_entries[0].score}")
        #     if len(all_entries) > 1:
        #         print(f"Last entry: Rank {all_entries[-1].rank}, Name: {all_entries[-1].name}, Score: {all_entries[-1].score}")
        # else:
        #     print("Full scoreboard is empty or could not be fetched.")

    except ScoreboardFetchError as e:
        print(f"Error fetching scoreboard: {e}")
    except UnauthorizedError:
        print("Error: Scoreboard access requires authentication on this platform.")
    except CTFInactiveError as e:
        print(f"Error: CTF or scoreboard is inactive: {e}")
    except CTFBridgeError as e:
        print(f"A CTFBridge error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())

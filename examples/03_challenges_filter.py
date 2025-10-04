import asyncio

from ctfbridge import create_client
from ctfbridge.exceptions import CTFBridgeError


async def main():
    client = await create_client("https://demo.ctfd.io")
    await client.auth.login(username="user", password="password")

    try:
        print("Fetching all challenges to demonstrate filtering...")
        all_challenges = await client.challenges.get_all(detailed=True, enrich=True)
        if not all_challenges:
            print("No challenges found to filter.")
            return
        print(f"Total challenges fetched: {len(all_challenges)}")

        # Example 1: Filter by category "Pwn" (case-insensitive for name_contains, exact for category)
        # Note: demo.ctfd.io might not have a "Pwn" category. Adjust as needed.
        # We'll use a category that likely exists, e.g., the category of the first challenge.
        example_category = all_challenges[0].category if all_challenges else "Miscellaneous"
        print(f"\nFiltering for category: '{example_category}'")
        pwn_challenges = await client.challenges.get_all(category=example_category, detailed=False)
        print(f"Found {len(pwn_challenges)} challenges in category '{example_category}':")
        for chal in pwn_challenges[:3]:
            print(f"  - {chal.name} ({chal.value} pts)")

        # Example 2: Filter by minimum points (e.g., >= 100 points)
        min_pts = 100
        print(f"\nFiltering for challenges with >= {min_pts} points...")
        high_value_challenges = await client.challenges.get_all(min_points=min_pts, detailed=False)
        print(f"Found {len(high_value_challenges)} challenges with at least {min_pts} points:")
        for chal in high_value_challenges[:3]:
            print(f"  - {chal.name} ({chal.value} pts)")

        # Example 3: Filter by solved status (e.g., unsolved challenges)
        # On demo.ctfd.io without login, 'solved' will likely be False for all.
        print("\nFiltering for unsolved challenges...")
        unsolved_challenges = await client.challenges.get_all(solved=False, detailed=False)
        print(f"Found {len(unsolved_challenges)} unsolved challenges:")
        for chal in unsolved_challenges[:3]:
            print(f"  - {chal.name} ({chal.value} pts, Solved: {chal.solved})")

        # Example 4: Filter by name containing "Web" (case-insensitive)
        search_term = "Web"
        print(f"\nFiltering for challenges with name containing '{search_term}'...")
        web_challenges_by_name = await client.challenges.get_all(
            name_contains=search_term, detailed=False
        )
        print(f"Found {len(web_challenges_by_name)} challenges with '{search_term}' in name:")
        for chal in web_challenges_by_name[:3]:
            print(f"  - {chal.name} ({chal.value} pts)")

        # Example 5: Combined filters - category "Web" (if exists) AND points > 50
        # Adjust category if "Web" doesn't exist on demo.ctfd.io
        target_category_for_combo = "Web"  # or another existing category
        # Check if this category exists, otherwise pick one
        if not any(c.category == target_category_for_combo for c in all_challenges):
            target_category_for_combo = (
                all_challenges[0].category if all_challenges else "Miscellaneous"
            )

        print(f"\nFiltering for category '{target_category_for_combo}' AND points > 50...")
        combined_filter_chals = await client.challenges.get_all(
            category=target_category_for_combo, min_points=51, detailed=False
        )
        print(f"Found {len(combined_filter_chals)} challenges matching combined filters:")
        for chal in combined_filter_chals[:3]:
            print(f"  - {chal.name} (Category: {chal.category}, Points: {chal.value})")

    except CTFBridgeError as e:
        print(f"A CTFBridge error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())

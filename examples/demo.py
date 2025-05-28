import asyncio

from ctfbridge import create_client


async def run_demo():
    print("Connecting to CTF platform...")

    client = await create_client("https://demo.ctfd.io")

    print("Logging in...")
    await client.auth.login(username="user", password="password")

    print("Fetching challenges...")
    challenges = await client.challenges.get_all(detailed=True)

    for chal in challenges:
        print(f"[{chal.category}] {chal.name} ({chal.value} pts)")

    if challenges:
        print("Submitting a fake flag to the first challenge...")
        result = await client.challenges.submit(challenges[0].id, "CTF{testflag}")
        print("Submission result:", result.message)

    print("Fetching scoreboard...")
    top = await client.scoreboard.get_top(5)
    for entry in top:
        print(f"{entry.rank}. {entry.name} - {entry.score} points")

    print("Done!")


if __name__ == "__main__":
    asyncio.run(run_demo())

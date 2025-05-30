import asyncio
from ctfbridge import create_client
from ctfbridge.exceptions import (
    CTFBridgeError,
    LoginError,
    SubmissionError,
    UnauthorizedError,
    CTFInactiveError,
    RateLimitError,
)


async def main():
    client = await create_client("https://demo.ctfd.io")

    username = "user"
    password = "password"

    challenge_id_to_submit = None
    flag_to_submit = "CTF{dummy_flag_for_testing}"  # Replace with a real flag if testing a solve

    try:
        # 1. Login
        print(f"Attempting to login as {username}...")
        await client.auth.login(username=username, password=password)
        print("Login successful!")

        # 2. Get a challenge ID to submit to
        # For a real scenario, you'd solve the challenge and know its ID.
        # Here, we'll just pick the first available challenge.
        print("Fetching challenges to get an ID...")
        challenges = await client.challenges.get_all(detailed=False)
        if not challenges:
            print("No challenges found. Cannot proceed with flag submission.")
            return
        challenge_id_to_submit = challenges[0].id
        challenge_name_to_submit = challenges[0].name
        print(
            f"Will attempt to submit a flag to challenge ID: {challenge_id_to_submit} ('{challenge_name_to_submit}')"
        )

        # 3. Submit the flag
        print(f"Submitting flag '{flag_to_submit}' to challenge ID {challenge_id_to_submit}...")
        result = await client.challenges.submit(
            challenge_id=challenge_id_to_submit, flag=flag_to_submit
        )

        print("\n--- Submission Result ---")
        print(f"Correct: {result.correct}")
        print(f"Message: {result.message}")
        print()

        if result.correct:
            print("Congratulations! Flag was correct.")
        else:
            print("Flag was incorrect or already submitted.")

    except LoginError as e:
        print(f"Login failed: {e}")
    except UnauthorizedError:
        print(
            "Error: Authentication is required for this action, but login might have failed silently or token expired."
        )
    except SubmissionError as e:
        print(f"Flag submission failed: {e.reason}")
        print(f"  Challenge ID: {e.challenge_id}, Flag: {e.flag}")
    except CTFInactiveError as e:
        print(f"CTF Inactive: {e}")
    except RateLimitError as e:
        print(f"Rate Limited: {e}. Retry after: {e.retry_after}s")
    except CTFBridgeError as e:
        print(f"A CTFBridge error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())

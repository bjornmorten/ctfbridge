from ctfbridge import get_client
from ctfbridge.exceptions import (
    ChallengeFetchError,
    LoginError,
    SessionExpiredError,
    SubmissionError,
)


def main():
    base_url = "https://s2gctf.ncr.ntnu.no/play/sfdsf/sdfsd/sdf/sdf"
    base_url = "https://umdctf.io/"
    # base_url = 'https://google.io'
    username = "admin"
    password = "password"
    token = "https://umdctf.io/login?token=d6iGcsa%2FA0JgyCXJ32hJHnlW4G5PHs9bMXQraaTDq38GYoNPMGwFQ9X28muR6MBbTNfmQZzGKYdHVNO4UYP2W7U8QwJlBpuue4%2FDENDfMZfNmS1U3JEA2Uksl9Av"
    base_url = "https://demo.ctfd.io"

    base_url = "https://umdctf.io/"
    # base_url = 'demo'
    # username = 'demo'
    # password = 'demo'

    base_url = "https://ctf.stair.ch/"

    client = get_client(base_url)

    try:
        print("[*] Logging in...")
        # client.login(username=username, password=password, token=token)
        print("[+] Login successful!")
    except LoginError as e:
        print(f"[-] Login failed: {e}")
        return

    try:
        print("\n[*] Fetching challenges...")
        challenges = client.challenges.get_all()
        print(f"[+] Found {len(challenges)} challenges!")

        for challenge in challenges[:2]:
            print(f"\n[*] Fetching details of a challenge: {challenge.name}")
            detailed = client.challenges.get_by_id(challenge.id)
            print(f"[+] Challenge Description: {detailed.description}")

            import time

            start = time.time()
            for attachment in challenge.attachments:
                print("\n[*] Downloading first attachment...")
                path = client.attachments.download(attachment, "/tmp/")
                print(f"[+] Attachment saved to {path}")
            print(challenge.name, time.time() - start)

            print("\n[*] Submitting fake flag to first challenge...")
            result = client.challenges.submit(challenge.id, "FAKE{test_flag}")
            if result.correct:
                print("[+] Flag correct! (this should not happen with a fake flag)")
            else:
                print(f"[-] Incorrect flag submission (expected): {result.message}")

        print("\n[*] Fetching leaderboard...")
        leaderboard = client.scoreboard.get_top(limit=0)
        for entry in leaderboard:
            print(f"[+] {entry.rank}. {entry.name} - {entry.score} points")

    except SessionExpiredError:
        print("[-] Session expired! Please login again.")
    except ChallengeFetchError as e:
        print(f"[-] Failed to fetch challenges: {e}")
    except SubmissionError as e:
        print(f"[-] Failed to submit flag: {e}")
    except Exception as e:
        print(f"[-] Unexpected error: {e}")


if __name__ == "__main__":
    main()

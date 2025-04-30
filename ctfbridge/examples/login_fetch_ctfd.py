from ctfbridge import CTFdClient
from ctfbridge.exceptions import RateLimitError, SessionExpiredError

client = CTFdClient("https://demo.ctfd.io")

try:
    client.login("admin", "password")
    challenges = client.get_challenges()

    for chal in challenges:
        print(f"[{chal.category}] {chal.name} ({chal.value} points)")

except SessionExpiredError:
    print("Session expired. Please re-login.")
except RateLimitError as e:
    print(f"Rate limit hit: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
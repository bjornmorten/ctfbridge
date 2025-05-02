from ctfbridge import DemoClient
from ctfbridge.exceptions import RateLimitError, SessionExpiredError

client = DemoClient("demo")

try:
    client.login("demo", "demo")
    challenges = client.challenges.get_all()

    for chal in challenges:
        print(f"[{chal.category}] {chal.name} ({chal.value} points)")

except SessionExpiredError:
    print("Session expired. Please re-login.")
except RateLimitError as e:
    print(f"Rate limit hit: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

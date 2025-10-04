"""
CLI entry point for checking the health of a live test instance.
"""

import argparse
import sys
import time

import httpx


def check_ctfd_health(client: httpx.Client) -> bool:
    """
    Checks if the CTFd instance is ready.

    A healthy CTFd instance is one that is not only listening but is also
    serving the main application, which could be either the setup page or
    the main CTF site.
    """
    try:
        # We use follow_redirects=True because a base URL might redirect
        # (e.g., http -> https)
        response = client.get("/", follow_redirects=True)
        # A successful response should contain text indicating it's CTFd
        # or be on the setup page.
        is_ready = response.status_code == 200 and (
            "CTFd" in response.text or "/setup" in str(response.url)
        )
        return is_ready
    except httpx.RequestError:
        # The service is not yet listening on the port.
        return False


def check_rctf_health(client: httpx.Client) -> bool:
    """
    Checks if the rCTF instance is ready.
    rCTF is healthy if its /api/v1/users/me endpoint responds,
    even with an auth error.
    """
    try:
        response = client.get("/api/v1/users/me")
        # rCTF returns 401 and a "badToken" error if healthy but not authenticated.
        # A connection error would mean it's not ready.
        return response.status_code == 401 and "badToken" in response.text
    except httpx.RequestError:
        return False


# --- Main Execution Logic ---

# A registry to map platform names to their health check functions
HEALTH_CHECKS = {
    "ctfd": check_ctfd_health,
    "rctf": check_rctf_health,
}


def main() -> None:
    """
    Main function to parse arguments and run the health check loop.
    """
    parser = argparse.ArgumentParser(
        description="Check the health of a live CTF instance for E2E tests."
    )
    parser.add_argument(
        "--platform",
        required=True,
        choices=HEALTH_CHECKS.keys(),
        help="The platform to health check.",
    )
    parser.add_argument("--url", required=True, help="Base URL of the live instance.")
    args = parser.parse_args()

    print(f"Checking health of {args.platform} at {args.url}...")

    # Select the correct health check function from the registry
    check_function = HEALTH_CHECKS[args.platform]

    with httpx.Client(base_url=args.url) as client:
        # Loop for a total of 2 minutes (60 retries * 2 seconds)
        for i in range(60):
            if check_function(client):
                print("Service is healthy. Continuing...")
                sys.exit(0)

            print(f"Waiting for service to become healthy... (attempt {i + 1}/60)")
            time.sleep(2)

    print("Service did not become healthy in time.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()

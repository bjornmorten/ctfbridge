import asyncio
import os
import tempfile
from ctfbridge import create_client
from ctfbridge.exceptions import CTFBridgeError, ChallengeFetchError, AttachmentDownloadError


async def main():
    client = await create_client("https://demo.ctfd.io")
    await client.auth.login(username="user", password="password")

    challenge_with_attachments = None

    try:
        print("Fetching challenges to find one with multiple attachments (or any attachments)...")
        challenges = await client.challenges.get_all(detailed=True, enrich=True)
        if not challenges:
            print("No challenges found.")
            return

        for chal in challenges:
            if chal.attachments:  # Could be one or more
                challenge_with_attachments = chal
                print(f"Found challenge '{chal.name}' with {len(chal.attachments)} attachment(s).")
                for att in chal.attachments:
                    print(f"  - Attachment: '{att.name}', URL: '{att.url}'")
                break  # Take the first challenge found with any attachments

        if not challenge_with_attachments:
            print("No challenges with attachments found on the platform.")
            return

        # Create a temporary directory to save the attachments
        # You can use a specific path like "./challenge_downloads" instead of tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            challenge_save_dir = os.path.join(
                tmpdir, challenge_with_attachments.name.replace(" ", "_")
            )  # Sanitize name for dir
            print(
                f"\nAttempting to download all attachments for '{challenge_with_attachments.name}' to {challenge_save_dir}..."
            )

            try:
                # The download_all method takes a list of Attachment objects
                downloaded_paths = await client.attachments.download_all(
                    attachments=challenge_with_attachments.attachments, save_dir=challenge_save_dir
                )

                if downloaded_paths:
                    print("Successfully downloaded the following files:")
                    for path in downloaded_paths:
                        print(f"  - {path}")
                        assert os.path.exists(path)
                else:
                    print(
                        "No files were downloaded. This might happen if all downloads failed or there were no valid attachments."
                    )

            except AttachmentDownloadError as e:
                # This might be raised if a global issue occurs, though individual errors are often logged and skipped by download_all
                print(f"A general error occurred during batch download: {e}")
            except Exception as e:
                print(f"An unexpected error occurred during download_all: {e}")

    except ChallengeFetchError as e:
        print(f"Error fetching challenges: {e}")
    except CTFBridgeError as e:
        print(f"A CTFBridge error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())

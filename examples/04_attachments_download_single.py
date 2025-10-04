import asyncio
import os
import tempfile

from ctfbridge import create_client
from ctfbridge.exceptions import AttachmentDownloadError, ChallengeFetchError, CTFBridgeError
from ctfbridge.models.challenge import Attachment


async def main():
    client = await create_client("https://demo.ctfd.io")
    await client.auth.login(username="user", password="password")

    attachment_to_download = None
    challenge_name = None

    try:
        print("Fetching challenges to find one with an attachment...")
        challenges = await client.challenges.get_all(
            detailed=True, has_attachments=True, enrich=True
        )
        if not challenges:
            print("No challenges found.")
            return

        for chal in challenges:
            if chal.attachments:
                attachment_to_download = chal.attachments[0]
                challenge_name = chal.name
                print(
                    f"Found challenge '{challenge_name}' with attachment: '{attachment_to_download.name}' ({attachment_to_download.url})"
                )
                break

        if not attachment_to_download:
            print("No challenges with attachments found")
            return

        # Create a temporary directory to save the attachment
        with tempfile.TemporaryDirectory() as tmpdir:
            print(
                f"\nAttempting to download attachment '{attachment_to_download.name}' to {tmpdir}..."
            )

            # Basic download
            try:
                saved_path = await client.attachments.download(
                    attachment_to_download, save_dir=tmpdir
                )
                print(f"Attachment downloaded successfully to: {saved_path}")
                assert os.path.exists(saved_path)
            except AttachmentDownloadError as e:
                print(f"Error downloading attachment: {e}")
            except Exception as e:
                print(f"An unexpected error occurred during basic download: {e}")

            # Download with a custom filename
            custom_filename = f"custom_{attachment_to_download.name}"
            print(
                f"\nAttempting to download attachment with custom name '{custom_filename}' to {tmpdir}..."
            )
            try:
                saved_path_custom = await client.attachments.download(
                    attachment_to_download, save_dir=tmpdir, filename=custom_filename
                )
                print(
                    f"Attachment downloaded successfully with custom name to: {saved_path_custom}"
                )
                assert os.path.exists(saved_path_custom)
                assert os.path.basename(saved_path_custom) == custom_filename
            except AttachmentDownloadError as e:
                print(f"Error downloading attachment with custom name: {e}")
            except Exception as e:
                print(f"An unexpected error occurred during custom filename download: {e}")

    except ChallengeFetchError as e:
        print(f"Error fetching challenges: {e}")
    except CTFBridgeError as e:
        print(f"A CTFBridge error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())

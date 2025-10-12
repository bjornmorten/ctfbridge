import logging
import asyncio

from ctfbridge.platforms.ctfd.services.challenge import CTFdChallengeService
from ctfbridge.exceptions.challenge import ChallengeFetchError
from ctfbridge.models.challenge import (
    Challenge,
    DownloadInfo,
    DownloadType,
    Attachment,
    AttachmentCollection,
)
from ctfbridge.platforms.pwncollege.utils.api import PwnCollegeService

logger = logging.getLogger(__name__)


class PwnCollegeChallengeService(CTFdChallengeService):
    def __init__(self, client):
        self._client = client
        self.svc = PwnCollegeService(client)

    @property
    def base_has_details(self) -> bool:
        return True

    async def _fetch_challenges(self) -> list[Challenge]:
        try:
            dojo_sections = await self.svc.get_dojo_sections()

            tasks = []
            for section in dojo_sections:
                for dojo in section.dojos:
                    tasks.append(self.svc.get_dojo_detailed(dojo))

            dojo_detailed_list = await asyncio.gather(*tasks)

            module_tasks = []
            for dojo_detailed in dojo_detailed_list:
                for module in dojo_detailed.modules:
                    module_tasks.append(self.svc.get_module_detailed(dojo_detailed, module))

            module_detailed_list = await asyncio.gather(*module_tasks)

            def make_challenge_object(chal):
                # TODO: improve to use both dojo_title, module_title and chal category
                category = chal.module_title
                return Challenge(
                    id=chal.id,
                    name=chal.title,
                    categories=[category],
                    description=chal.description,
                    attachments=AttachmentCollection(
                        attachments=[
                            Attachment(
                                download_info=DownloadInfo(
                                    type=DownloadType.SSH,
                                    host="dojo.pwn.college",
                                    port=22,
                                    username="hacker",
                                ),
                            )
                        ]
                    ),
                    value=1,
                )

            challenges = [
                make_challenge_object(chal)
                for module in module_detailed_list
                for chal in module.challenges
            ]
            return challenges

        except Exception as e:
            logger.debug("Error while fetching or parsing challenges", exc_info=e)
            raise ChallengeFetchError("Failed to fetch or parse challenges from pwn.college") from e

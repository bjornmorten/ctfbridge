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
            if self._client.dojo_slug:
                dojo = await self.svc.get_dojo_detailed(self._client.dojo_slug)
                if self._client.module_slug:
                    module = await self.svc.get_module_detailed(dojo.slug, self._client.module_slug)
                    modules = [module]
                else:
                    modules = [
                        await self.svc.get_module_detailed(dojo.slug, m.slug) for m in dojo.modules
                    ]
            else:
                dojo_sections = await self.svc.get_dojo_sections()
                dojo_detailed_list = await asyncio.gather(
                    *[
                        self.svc.get_dojo_detailed(dojo.slug)
                        for section in dojo_sections
                        for dojo in section.dojos
                    ]
                )
                modules = [
                    module
                    for dojo_detailed in dojo_detailed_list
                    for module in await asyncio.gather(
                        *[
                            self.svc.get_module_detailed(dojo_detailed.slug, m.slug)
                            for m in dojo_detailed.modules
                        ]
                    )
                ]

            challenges = [
                self._make_challenge_object(chal)
                for module in modules
                for chal in module.challenges
            ]
            return challenges

        except Exception as e:
            logger.debug("Error while fetching or parsing challenges", exc_info=e)
            raise ChallengeFetchError("Failed to fetch or parse challenges from pwn.college") from e

    def _make_challenge_object(self, chal):
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
                            path="/challenge/",
                            extra={
                                "pwncollege_dojo": chal.dojo_slug,
                                "pwncollege_module": chal.module_slug,
                                "pwncollege_challenge": chal.slug,
                            },
                        ),
                    )
                ]
            ),
            value=1,
        )

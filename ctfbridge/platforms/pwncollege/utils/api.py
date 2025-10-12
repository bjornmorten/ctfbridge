from ctfbridge.platforms.pwncollege.models.models import Dojo, Module, DojoSection
from ctfbridge.platforms.pwncollege.utils.parsers import (
    parse_dojos_list,
    parse_dojo_detail,
    parse_module_detail,
)
from ctfbridge.core.client import CoreCTFClient
from ctfbridge.exceptions import UnauthorizedError


class PwnCollegeService:
    def __init__(self, client: CoreCTFClient):
        self.client = client

    async def get_dojo_sections(self) -> list[DojoSection]:
        """
        Fetch and parse the list of available dojos.

        Returns:
            List of Dojo objects with basic metadata (title, url, etc.).
        """
        response = await self.client.get("/dojos", timeout=15)
        response.raise_for_status()
        html = response.text
        dojos = parse_dojos_list(html)
        return dojos

    async def get_dojo_detailed(self, dojo_slug: str) -> Dojo:
        """
        Fetch and parse a single dojo.

        Example:
            service.get_dojo("program-security")

        Args:
            slug: The dojo's URL slug, e.g. "program-security".

        Returns:
            A fully populated Dojo object
        """
        response = await self.client.get(f"/{dojo_slug}", timeout=15)
        response.raise_for_status()
        dojo = parse_dojo_detail(response.text)
        return dojo

    async def get_module_detailed(self, dojo_slug: str, module_slug: str) -> Module:
        """
        Parse a module detail page (e.g. /welcome/welcome) into a Module object
        with full Challenge entries.
        """
        response = await self.client.get(f"/{dojo_slug}/{module_slug}", timeout=15)
        response.raise_for_status()
        module = parse_module_detail(response.text)
        return module

    async def add_ssh_key(self, public_key) -> bool:
        response = await self.client.post(
            "/pwncollege_api/v1/ssh_key", json={"ssh_key": public_key.decode()}
        )
        if response.status_code == 403:
            raise UnauthorizedError("You need to be logged in to add SSH keys")
        response.raise_for_status()
        data = response.json()
        return data["success"]

    async def remove_ssh_key(self, public_key) -> bool:
        response = await self.client.delete(
            "/pwncollege_api/v1/ssh_key", json={"ssh_key": public_key}
        )
        response.raise_for_status()
        data = response.json()
        return data["success"]

    async def start_ondemand_docker(
        self, dojo: str, module: str, challenge: str, practice: bool = False
    ) -> bool:
        response = await self.client.post(
            "/pwncollege_api/v1/docker",
            json={"challenge": challenge, "dojo": dojo, "module": module, "practice": practice},
        )
        if response.status_code == 403:
            raise UnauthorizedError("You need to be logged in to start services")
        response.raise_for_status()
        data = response.json()
        return data["success"]

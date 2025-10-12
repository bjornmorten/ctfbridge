from bs4 import BeautifulSoup
from ctfbridge.platforms.pwncollege.models.models import Dojo, Module, DojoSection, Challenge
from ctfbridge.platforms.pwncollege.utils.parsers import (
    parse_dojos_list,
    parse_dojo_detail,
    parse_module_detail,
)
from ctfbridge.core.client import CoreCTFClient


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

    async def get_dojo_detailed(self, dojo: Dojo) -> Dojo:
        """
        Fetch and parse a single dojo.

        Example:
            service.get_dojo("program-security")

        Args:
            slug: The dojo's URL slug, e.g. "program-security".

        Returns:
            A fully populated Dojo object
        """
        response = await self.client.get(f"/{dojo.slug}", timeout=15)
        response.raise_for_status()
        dojo = parse_dojo_detail(response.text)
        return dojo

    async def get_module_detailed(self, dojo: Dojo, module: Module) -> Module:
        """
        Parse a module detail page (e.g. /welcome/welcome) into a Module object
        with full Challenge entries.
        """
        response = await self.client.get(f"/{dojo.slug}/{module.slug}", timeout=15)
        response.raise_for_status()
        module = parse_module_detail(response.text)
        return module

    async def add_ssh_key(self, public_key) -> bool:
        response = await self.client.post(
            "/pwncollege_api/v1/ssh_key", json={"ssh_key": public_key}
        )
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

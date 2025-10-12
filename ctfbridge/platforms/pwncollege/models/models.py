from pydantic import BaseModel


class Challenge(BaseModel):
    id: str
    title: str
    slug: str
    category: str | None
    description: str
    dojo_title: str
    module_title: str
    dojo_slug: str
    module_slug: str


class Module(BaseModel):
    # "Using the Dojo" / "Joining the Discord" / ...
    title: str
    # "welcome" / "discord" / ...
    slug: str

    challenges: list[Challenge] = []


class Dojo(BaseModel):
    # "Start Here" / "Linux Luminarium" / "Computing 101" / ...
    title: str
    # "welcome" / "linux-luminarium" / "computing-101" / ...
    slug: str

    modules: list[Module] = []


class DojoSection(BaseModel):
    # "Getting Started" / "Core Material" / "Community Material" / ...
    title: str
    dojos: list[Dojo]

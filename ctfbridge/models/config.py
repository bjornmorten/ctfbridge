from pydantic import BaseModel, Field


class CTFConfig(BaseModel):
    """Represents the configuration settings of a CTF platform."""

    ctf_name: str = Field(..., description="The name of the CTF event or platform.")
    user_mode: str = Field(..., description="The participation mode (e.g., 'teams', 'users').")
    theme: str | None = Field(default=None, description="The UI theme name, if customizable.")
    version: str | None = Field(default=None, description="The platform version identifier.")

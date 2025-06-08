from pydantic import BaseModel, Field


class Capabilities(BaseModel):
    """
    Represents the features supported by a ctfbridge platform client.
    """

    login: bool = Field(False, description="Indicates if the client supports authentication.")
    submit_flag: bool = Field(
        False, description="Indicates if the client supports submitting flags."
    )
    view_scoreboard: bool = Field(
        False, description="Indicates if the client supports viewing the scoreboard."
    )
    list_challenges: bool = Field(
        True, description="Indicates if the client supports listing challenges."
    )

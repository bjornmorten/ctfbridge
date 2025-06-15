from pydantic import BaseModel, Field


class Capabilities(BaseModel):
    """
    Represents the features supported by a ctfbridge platform client.
    """

    # --- Core Authentication & Session ---
    login: bool = Field(
        default=False, description="Indicates if the client supports authentication."
    )
    session_persistence: bool = Field(
        default=True,
        description="Indicates if the session (cookies/tokens) can be reliably saved and loaded.",
    )

    # --- Team & User Management ---
    view_team_information: bool = Field(
        default=False,
        description="Indicates if the client can fetch details about a team, such as its members and rank.",
    )
    view_user_profile: bool = Field(
        default=False,
        description="Indicates if the client can fetch details for the authenticated user's profile.",
    )

    # --- CTF Event Interaction ---
    view_ctf_details: bool = Field(
        default=False,
        description="Indicates if the client can fetch metadata about the CTF event itself (e.g., start/end times, rules).",
    )
    view_announcements: bool = Field(
        default=False,
        description="Indicates if the client can fetch broadcast announcements for the CTF.",
    )
    view_scoreboard: bool = Field(
        default=False, description="Indicates if the client supports viewing the scoreboard."
    )

    # --- Challenge Interaction ---
    view_challenges: bool = Field(
        default=False, description="Indicates if the client supports listing challenges."
    )
    submit_flags: bool = Field(
        default=False, description="Indicates if the client supports submitting flags."
    )
    download_attachments: bool = Field(
        default=True, description="Indicates if the client can download challenge attachments."
    )
    manage_challenge_instances: bool = Field(
        default=False,
        description="Indicates if the client can start, stop, or get connection info for on-demand challenge instances (e.g., Docker containers).",
    )

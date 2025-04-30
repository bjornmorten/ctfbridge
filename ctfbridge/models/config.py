from typing import Optional

from pydantic import BaseModel


class CTFConfig(BaseModel):
    ctf_name: str
    user_mode: str
    theme: Optional[str] = None
    version: Optional[str] = None



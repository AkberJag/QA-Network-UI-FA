from typing import Literal

from pydantic import BaseModel


class Token(BaseModel):
    """Base token schema"""

    access_token: str
    toke_type: Literal["bearer"]

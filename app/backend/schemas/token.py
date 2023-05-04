from typing import Literal

from pydantic import BaseModel


class Token(BaseModel):
    """Base token schema"""

    access_token: str
    token_type: Literal["bearer"]

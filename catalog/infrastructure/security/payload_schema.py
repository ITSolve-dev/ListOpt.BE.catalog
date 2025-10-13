from pydantic import Field

from ._base import Payload


class PayloadSchema(Payload):
    id: int = Field(alias="sub")
    email: str
    role: str

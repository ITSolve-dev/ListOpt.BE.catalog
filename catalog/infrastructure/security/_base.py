from pydantic import BaseModel
from pydantic.dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BaseUser:
    role: str


class Payload(BaseModel):
    pass

from ._base import Payload


class PayloadSchema(Payload):
    id: int
    email: str
    role: str

from typing import Sequence

import jwt
from pydantic import BaseModel

from catalog.infrastructure.security._base import Payload


class JwtEncoder[PayloadType: BaseModel = Payload]:
    def __init__(
        self, key: str, algorithms: Sequence[str] = ["HS256"]
    ) -> None:
        self._key = key
        self._algorithms = algorithms

    def encode(self, payload: PayloadType) -> str:
        token = jwt.encode(
            payload=payload.model_dump(),
            key=self._key,
            algorithm=self._algorithms[0],
        )
        return token

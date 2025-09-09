from typing import Sequence

import jwt
from pydantic import BaseModel

from catalog.infrastructure.security._base import Payload


class JwtDecoder[ReturnType: BaseModel = Payload]:
    def __init__(
        self,
        schema: type[ReturnType],
        key: str,
        algorithms: Sequence[str] = ["HS256"],
    ) -> None:
        self._schema = schema
        self._key = key
        self._algorithms = algorithms

    def decode(self, token: str) -> ReturnType:
        payload = jwt.decode(token, self._key, algorithms=self._algorithms)
        return self._schema.model_validate(payload)

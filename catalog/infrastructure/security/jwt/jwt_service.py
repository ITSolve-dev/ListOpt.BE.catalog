from pydantic import BaseModel

from .._base import Payload
from .jwt_decoder import JwtDecoder
from .jwt_encoder import JwtEncoder


class JwtService[SchemaType: BaseModel = Payload]:
    def __init__(
        self,
        jwt_decoder: JwtDecoder[SchemaType],
        jwt_encoder: JwtEncoder[SchemaType],
    ):
        self.__jwt_decoder = jwt_decoder
        self.__jwt_encoder = jwt_encoder

    def decode(self, token: str) -> SchemaType:
        return self.__jwt_decoder.decode(token)

    def encode(self, payload: SchemaType) -> str:
        return self.__jwt_encoder.encode(payload)

    @property
    def jwt_decoder(self) -> JwtDecoder[SchemaType]:
        return self.__jwt_decoder

    @property
    def jwt_encoder(self) -> JwtEncoder[SchemaType]:
        return self.__jwt_encoder

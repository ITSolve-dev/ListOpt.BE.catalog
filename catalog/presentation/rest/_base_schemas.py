import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Schema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, extra="forbid", arbitrary_types_allowed=True
    )


class ResponseSchema(Schema):
    __info__: str | None = None
    info: str | None | None = "Default response"
    timestamp: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )


class SuccessResponse(ResponseSchema):
    __info__ = "Success response"
    ok: bool = True


class FailedResponse(ResponseSchema):
    __info__ = "Failed response"
    ok: bool = False
    error: str = Field(examples=["catalog.layer.error_code"])
    ctx: dict[str, Any] | None = None


class RequestSchema(Schema): ...


class PaginateResponse[T](SuccessResponse):
    __info__ = "Default pagination response schema"
    items: list[T]
    page: int
    size: int
    total: int
    pages: int

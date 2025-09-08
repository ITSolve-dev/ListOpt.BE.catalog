from contextlib import asynccontextmanager
from typing import cast

import uvicorn
from pydantic import BaseModel
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    BaseUser,
    UnauthenticatedUser,
)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from starlette.types import ExceptionHandler

from catalog import error_names, scopes
from catalog.domain.exceptions import BaseError, CartAlreadyExistsError
from catalog.infrastructure.db.orm import (
    map_entities_on_tables,
    mapper_registry,
)
from catalog.infrastructure.executable import ExecutableProtocol
from catalog.infrastructure.security import (
    JwtService,
    PayloadSchema,
    PermissionService,
)
from catalog.presentation.rest import (
    cart_router,
    category_router,
    health_router,
    product_router,
)
from catalog.presentation.rest._base_schemas import FailedResponse
from fastapi import Depends, FastAPI, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .jwt_bearer_security import JWTBearerSecurity


class BaseAuthenticationBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> tuple[AuthCredentials, BaseUser] | None:
        return AuthCredentials(["unauthenticated"]), UnauthenticatedUser()


class ProjectSettings(BaseModel):
    name: str
    version: str
    description: str


class ServerSettings(BaseModel):
    host: str
    port: int
    reload: bool
    workers: int
    root_path: str
    root_path_in_servers: bool
    prefix: str
    allow_origins: list[str]
    allow_credentials: bool
    allow_methods: list[str]
    allow_headers: list[str]


class HTTPAppConfig(ServerSettings, ProjectSettings):
    pass


class HTTPApp(FastAPI, ExecutableProtocol):
    def __init__(
        self,
        jwt_service: JwtService[PayloadSchema],
        permission_service: PermissionService,
        *args,
        server_settings: dict,
        project_settings: dict,
        **kwargs,
    ):
        self._config = HTTPAppConfig.model_validate(
            {**server_settings, **project_settings}
        )
        super().__init__(
            *args,
            **kwargs,
            title=self._config.name,
            description=self._config.description,
            version=self._config.version,
            lifespan=self.lifespan,
            responses={
                400: {
                    "model": FailedResponse,
                    "description": FailedResponse.__info__,
                },
                422: {"model": list[FailedResponse]},
            },
        )
        self._jwt_service = jwt_service
        self._permission_service = permission_service
        self._configure_routers()
        self._configure_middlewares()
        self._configure_error_handlers()
        self.add_middleware(
            AuthenticationMiddleware, backend=BaseAuthenticationBackend()
        )

    @asynccontextmanager
    async def lifespan(self, *args, **kwargs):
        map_entities_on_tables()
        yield
        mapper_registry.dispose()

    def run(self, *args, **kwargs):
        uvicorn.run(
            "main:http_app",
            *args,
            workers=self._config.workers,
            reload=self._config.reload,
            host=self._config.host,
            port=self._config.port,
            **kwargs,
        )

    def _configure_routers(self):
        self.include_router(health_router)
        self.include_router(
            cart_router,
            dependencies=[Depends(self.__get_jwt_bearer_security())],
        )
        self.include_router(
            category_router,
            dependencies=[Depends(self.__get_jwt_bearer_security())],
        )
        self.include_router(
            product_router,
            dependencies=[Depends(self.__get_jwt_bearer_security())],
        )

    def _configure_cors(self): ...

    def _configure_middlewares(self):
        self._configure_cors()

    def configure_logger(self): ...

    def _configure_error_handlers(self):
        self.add_exception_handler(BaseError, self._error_handler)
        self.add_exception_handler(
            CartAlreadyExistsError,
            self._error_handler_factory(status=status.HTTP_409_CONFLICT),
        )
        self.add_exception_handler(
            RequestValidationError,
            self._override_validation_exception,
        )

    def _error_handler_factory(self, status: int) -> ExceptionHandler:
        async def _handler(_: Request, e: Exception) -> Response:
            exc = cast(BaseError, e)
            response = FailedResponse(
                ctx=exc.ctx, error=exc.code, info=exc.description
            )
            return JSONResponse(
                content=jsonable_encoder(response, exclude_none=True),
                status_code=status,
            )

        return _handler

    def _override_validation_exception(
        self, _: Request, e: Exception
    ) -> Response:
        exc = cast(RequestValidationError, e)
        response = []
        for error in exc.errors():
            code = (
                f"catalog.{scopes.PRESENTATION}.{error_names.VALIDATION_ERROR}"
            )
            type = error.get("type", None)
            if type:
                code += f".{type}"
            response.append(
                FailedResponse(
                    ctx=dict(loc=error.get("loc", [])),
                    error=code,
                    info=error.get("msg", None),
                )
            )
        return JSONResponse(
            content=jsonable_encoder(response, exclude_none=True),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    async def _error_handler(self, _: Request, e: Exception) -> Response:
        exc = cast(BaseError, e)
        response = FailedResponse(
            ctx=exc.ctx, error=exc.code, info=exc.description
        )
        statuses: dict[str, int] = {
            error_names.NOT_FOUND: status.HTTP_404_NOT_FOUND,
            error_names.ALREADY_EXISTS: status.HTTP_409_CONFLICT,
            error_names.UNKNOWN: status.HTTP_400_BAD_REQUEST,
            error_names.PERMISSION_DENIED: status.HTTP_403_FORBIDDEN,
            error_names.VALIDATION_ERROR: status.HTTP_422_UNPROCESSABLE_ENTITY,
        }
        return JSONResponse(
            content=jsonable_encoder(response, exclude_none=True),
            status_code=statuses.get(exc.error, status.HTTP_400_BAD_REQUEST),
        )

    def __get_jwt_bearer_security(self):
        return JWTBearerSecurity(
            jwt_decoder=self._jwt_service.jwt_decoder,
            permission_service=self._permission_service,
        )

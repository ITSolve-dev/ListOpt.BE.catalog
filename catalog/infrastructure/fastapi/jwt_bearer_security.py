from pydantic import ValidationError
from starlette.authentication import UnauthenticatedUser

from catalog.infrastructure.security import (
    JwtDecoder,
    PayloadSchema,
    PermissionService,
)
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .user import User


class JWTBearerSecurity(HTTPBearer):
    def __init__(
        self,
        *,
        jwt_decoder: JwtDecoder[PayloadSchema],
        permission_service: PermissionService,
        bearer_format: str = "Bearer",
        scheme_name: str = "JWT Bearer",
        description: str = "Authentication and authorization provider",
    ) -> None:
        super().__init__(
            bearerFormat=bearer_format,
            scheme_name=scheme_name,
            description=description,
            auto_error=False,
        )
        self.jwt_decoder = jwt_decoder
        self.permission_service = permission_service

    async def __call__(
        self, request: Request
    ) -> HTTPAuthorizationCredentials | None:
        credentials = await super().__call__(request)
        if credentials is None:
            request.scope["user"] = UnauthenticatedUser()
            raise HTTPException(status_code=401, detail="Unauthorized")
        try:
            payload = self.jwt_decoder.decode(credentials.credentials)
        except ValidationError as e:
            raise HTTPException(status_code=401, detail="Invalid token") from e
        email = payload.email
        role = payload.role  # from payload or request from users API
        user = User(email=email, role=role, id=payload.id)
        request.scope["user"] = user
        has_access = self.permission_service.check(
            user, request.url.path, request.method
        )
        if not has_access:
            raise HTTPException(status_code=403, detail="Forbidden")
        return credentials

from pydantic.dataclasses import dataclass
from starlette.authentication import BaseUser as StarletteBaseUser

from catalog.infrastructure.security import BaseUser as UserWithRole


@dataclass(frozen=True, slots=True)
class User(UserWithRole, StarletteBaseUser):
    id: int
    email: str

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.email

    @property
    def identity(self) -> str:
        return self.email

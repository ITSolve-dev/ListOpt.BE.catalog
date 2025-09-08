import logging
from typing import Any

import casbin
from pydantic import BaseModel

from catalog.infrastructure.security._base import BaseUser

logger = logging.getLogger(__name__)


class PermissionsConfig(BaseModel):
    model: str = "model.conf"
    policy: str = "policy.csv"
    log: bool = False


class PermissionService:
    def __init__(self, config: dict[str, Any]) -> None:
        self._config = PermissionsConfig.model_validate(config)
        self.enforcer = casbin.Enforcer(
            self._config.model,
            self._config.policy,
            enable_log=self._config.log,
        )

    def check(self, user: BaseUser, resource: str, action: str) -> bool:
        return self.enforcer.enforce(user.role, resource, action)

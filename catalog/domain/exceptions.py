from dataclasses import dataclass, field

from catalog import error_names, scopes
from catalog.domain import names
from catalog.exceptions import BaseError


@dataclass(frozen=True, kw_only=True, slots=True)
class CatalogError(BaseError):
    app: str = field(default="catalog", init=False)


@dataclass(frozen=True, kw_only=True, slots=True)
class CatalogDomainError(CatalogError):
    entity: str

    @property
    def layer(self) -> str:
        return f"{scopes.DOMAIN}.{self.entity}"


@dataclass(frozen=True, kw_only=True, slots=True)
class CartError(CatalogDomainError):
    entity: str = field(default=names.CART, init=False)


@dataclass(frozen=True, kw_only=True, slots=True)
class ProductError(CatalogDomainError):
    entity: str = field(default=names.PRODUCT, init=False)


@dataclass(frozen=True, kw_only=True, slots=True)
class CategoryError(CatalogDomainError):
    entity: str = field(default=names.CATEGORY, init=False)


@dataclass(frozen=True, kw_only=True, slots=True)
class CartAlreadyExistsError(CartError):
    error: str = field(default=error_names.ALREADY_EXISTS, init=False)


@dataclass(frozen=True, kw_only=True, slots=True)
class CartNotFoundError(CartError):
    error: str = field(default=error_names.NOT_FOUND, init=False)


@dataclass(frozen=True, kw_only=True, slots=True)
class CartGetError(CartError):
    error: str = field(default=error_names.RETRIEVE_ERROR, init=False)


@dataclass(frozen=True, kw_only=True, slots=True)
class CartSaveError(CartError):
    error: str = field(default=error_names.SAVE_ERROR, init=False)


@dataclass(frozen=True, kw_only=True, slots=True)
class CategoryNotFoundError(CategoryError):
    error: str = field(default=error_names.NOT_FOUND, init=False)


@dataclass(frozen=True, kw_only=True, slots=True)
class ProductNotFoundError(ProductError):
    error: str = field(default=error_names.NOT_FOUND, init=False)


@dataclass(frozen=True, kw_only=True, slots=True)
class CartAlreadyHaveProductsError(CartError):
    error: str = field(default=error_names.ALREADY_EXISTS, init=False)


@dataclass(frozen=True, kw_only=True, slots=True)
class CartNotFoundProductsError(CartError):
    error: str = field(default=error_names.NOT_FOUND, init=False)

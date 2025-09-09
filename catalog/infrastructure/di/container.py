from dependency_injector import containers, providers

from catalog.application.commands import (
    AddCartCommand,
    AddProductCommand,
    AddProductsToCartCommand,
    ChangeQuantitiesProductsInCartCommand,
    RemoveProductsFromCartCommand,
)
from catalog.application.queries import (
    GetCartByUserQuery,
    GetCategoriesQuery,
    GetProductQuery,
    PaginateProductsQuery,
)
from catalog.domain.ports.uow import AbstractUnitOfWork
from catalog.domain.services import (
    CartService,
    CategoryService,
    ProductService,
)
from catalog.infrastructure.db.connection import DBConnection, IDBConnection
from catalog.infrastructure.db.uow import SqlAlchemyUnitOfWork
from catalog.infrastructure.executable import ExecutableProtocol
from catalog.infrastructure.fastapi import HTTPApp
from catalog.infrastructure.runner import Runner
from catalog.infrastructure.security import (
    JwtDecoder,
    JwtEncoder,
    JwtService,
    PayloadSchema,
    PermissionService,
)
from catalog.infrastructure.settings import get_settings


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["catalog.presentation.rest"]
    )
    config = providers.Configuration(pydantic_settings=[get_settings()])
    log_config = providers.Configuration(yaml_files=["logger.yml"])
    jwt_encoder = providers.Singleton[JwtEncoder[PayloadSchema]](
        JwtEncoder, key=config.jwt.SIGNING_KEY.required()
    )
    jwt_decoder = providers.Singleton[JwtDecoder[PayloadSchema]](
        JwtDecoder, key=config.jwt.SIGNING_KEY.required(), schema=PayloadSchema
    )
    jwt_service = providers.Singleton[JwtService[PayloadSchema]](
        JwtService, jwt_decoder=jwt_decoder, jwt_encoder=jwt_encoder
    )
    permission_service = providers.Singleton[PermissionService](
        PermissionService, config=config.permissions
    )
    http_app = providers.Singleton[ExecutableProtocol](
        HTTPApp,
        permission_service=permission_service,
        jwt_service=jwt_service,
        server_settings=config.server,
        project_settings=config.project,
    )
    runner = providers.Singleton[Runner](Runner, http_app=http_app)

    db_connection = providers.Singleton[IDBConnection](
        DBConnection,
        url=config.database.URL.required(),
        config=config.database,
    )

    uow = providers.Singleton[AbstractUnitOfWork](
        SqlAlchemyUnitOfWork,
        db_connection=db_connection,
    )

    cart_service = providers.Singleton[CartService](
        CartService,
        uow=uow,
    )
    category_service = providers.Singleton[CategoryService](
        CategoryService,
        uow=uow,
    )
    product_service = providers.Singleton[ProductService](
        ProductService,
        uow=uow,
    )

    get_cart_by_user_query = providers.Singleton[GetCartByUserQuery](
        GetCartByUserQuery,
        cart_service=cart_service,
    )
    add_cart_command = providers.Singleton[AddCartCommand](
        AddCartCommand,
        cart_service=cart_service,
    )
    get_categories_query = providers.Singleton[GetCategoriesQuery](
        GetCategoriesQuery,
        uow=uow,
    )
    get_product_query = providers.Singleton[GetProductQuery](
        GetProductQuery,
        uow=uow,
    )
    paginate_products_query = providers.Singleton[PaginateProductsQuery](
        PaginateProductsQuery,
        uow=uow,
    )
    add_product_command = providers.Singleton[AddProductCommand](
        AddProductCommand,
        category_service=category_service,
        product_service=product_service,
    )
    add_products_to_cart_command = providers.Singleton[
        AddProductsToCartCommand
    ](
        AddProductsToCartCommand,
        cart_service=cart_service,
        product_service=product_service,
    )
    remove_products_from_cart_command = providers.Singleton[
        RemoveProductsFromCartCommand
    ](
        RemoveProductsFromCartCommand,
        cart_service=cart_service,
    )
    change_quantities_products_in_cart = providers.Singleton[
        ChangeQuantitiesProductsInCartCommand
    ](
        ChangeQuantitiesProductsInCartCommand,
        cart_service=cart_service,
    )

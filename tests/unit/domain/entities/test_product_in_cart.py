from catalog.domain.entities import Product, ProductInCart
from catalog.domain.value_objects import Quantity


class TestProductInCart:
    def test_product_in_cart_creation(self, product_in_cart: ProductInCart):
        assert product_in_cart

    def test_product_in_cart_creation_default(self, product: Product):
        product_in_cart = ProductInCart(product=product, quantity=Quantity(1))
        assert product_in_cart.quantity == 1

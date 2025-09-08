from catalog.domain.entities import ProductInCart
from catalog.domain.value_objects import Quantity


class TestProductInCart:
    def test_product_in_cart_creation(self, product_in_cart):
        assert product_in_cart

    def test_product_in_cart_creation_default(self, product):
        product = ProductInCart(product=product, quantity=Quantity(1))
        assert product.quantity == 1

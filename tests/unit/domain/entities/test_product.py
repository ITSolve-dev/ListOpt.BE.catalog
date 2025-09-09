from catalog.domain.entities import Product


class TestProduct:
    def test_product_creation(self, product: Product):
        assert product

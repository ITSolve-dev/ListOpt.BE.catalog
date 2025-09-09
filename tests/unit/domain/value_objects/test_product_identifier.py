from catalog.domain.value_objects import ProductIdentifier


class TestProductIdentifier:
    def test_product_identifier_creation(
        self, product_identifier: ProductIdentifier
    ):
        assert product_identifier

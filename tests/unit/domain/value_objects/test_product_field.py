from catalog.domain.entities import ProductField


class TestProductField:
    def test_product_field_creation(self, product_field: ProductField) -> None:
        assert product_field

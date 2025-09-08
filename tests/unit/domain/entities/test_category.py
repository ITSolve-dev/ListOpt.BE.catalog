from catalog.domain.entities import Category


class TestCategory:
    def test_category_creation(self, category: Category):
        assert category

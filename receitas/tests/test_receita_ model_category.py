

from django.core.exceptions import ValidationError

from .test_receita_base import ReceitaTestBase


class CategoryModelTest(ReceitaTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category Testing'
        )
        return super().setUp()

    def test_category_string_representation(self):
        self.assertEqual(str(self.category), self.category.name)

    def test_category_name_max_length(self):
        self.category.name = 'a'*66

        with self.assertRaises(ValidationError):
            self.category.full_clean()

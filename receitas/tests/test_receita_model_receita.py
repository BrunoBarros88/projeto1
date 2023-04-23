import tempfile

from django.core.exceptions import ValidationError
from parameterized import parameterized
from PIL import Image

from .test_receita_base import Receita, ReceitaTestBase


class ReceitaModelTest(ReceitaTestBase):
    def setUp(self) -> None:
        self.image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        with open(self.image, 'w') as f:
            Image.new('RGB', (100, 100)).save(f, 'jpeg')
        self.receita = self.make_receita()
        return super().setUp()

    @parameterized.expand([('title', 65),
                           ('description', 200),
                           ('preparation_time_unit', 65),
                           ('servings_unit', 65)])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.receita, field, 'a'*(max_length+1))

        with self.assertRaises(ValidationError):
            self.receita.full_clean()

    def make_receita_no_defaults(self):
        receita = Receita(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time_unit='10 Minutes',
            servings_unit='5 servings',
            preparation_steps='Recipe Preparation Steps',
            cover=self.image
        )
        receita.full_clean()
        receita.save()
        return receita

    def test_receita_preparation_steps_is_html_is_false_by_default(self):
        receita = self.make_receita_no_defaults()
        self.assertFalse(receita.preparation_steps_is_html,
                         msg='Preparations steps is html is FALSE')

    def test_receita_is_published_is_false_by_default(self):
        receita = self.make_receita_no_defaults()
        self.assertFalse(receita.is_published, msg='Is published is FALSE')

    def test_receita_string_representation(self):
        needed = 'Testing Representation'
        self.receita.title = needed
        self.receita.full_clean()
        self.receita.save()
        self.assertEqual(str(self.receita), needed)

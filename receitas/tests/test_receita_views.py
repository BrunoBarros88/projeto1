

from django.urls import resolve, reverse

from receitas.views import (RecipeDetail, RecipeListViewCategory,
                            RecipeListViewHome, RecipeListViewSearch)

from .test_receita_base import ReceitaTestBase


class ReceitaViewsTest(ReceitaTestBase):

    def test_receita_home_view_function_is_correct(self):
        url = reverse('receitas:home')
        view = resolve(url).func.view_class
        self.assertIsInstance(view(), RecipeListViewHome)

    def test_receita_category_view_function_is_correct(self):
        url = reverse('receitas:category', kwargs={'category_id': 1})
        view = resolve(url).func.view_class
        self.assertIsInstance(view(), RecipeListViewCategory)

    def test_receita_detail_view_function_is_correct(self):
        url = reverse('receitas:receita', kwargs={'pk': 1})
        view = resolve(url).func.view_class
        self.assertIsInstance(view(), RecipeDetail)

    def test_receita_search_view_function_is_correct(self):
        url = reverse('receitas:search', )
        view = resolve(url).func.view_class
        self.assertIsInstance(view(), RecipeListViewSearch)

    def test_receita_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('receitas:home'))
        self.assertEqual(response.status_code, 200)

    def test_receita_home_view_loads_correct_template(self):
        response = self.client.get(reverse('receitas:home'))
        self.assertTemplateUsed(response, 'receitas/home.html')

    def test_receita_detail_view_returns_404_if_no_receitas_found(self):
        response = self.client.get(
            reverse('receitas:receita', kwargs={'pk': 1080})
        )
        self.assertEqual(response.status_code, 404)

    def test_receita_home_template_loads_receitas(self):
        self.make_receita()

        response = self.client.get(reverse('receitas:home'))
        content = response.content.decode('utf-8')
        response_context_receitas = response.context['receitas']

        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_receitas), 1)

    def test_receita_category_template_loads_receitas(self):
        needed_title = 'This is a category test'
        # Create recipe for this test
        self.make_receita(title=needed_title)

        response = self.client.get(reverse('receitas:category', args=(1,)))
        content = response.content.decode('utf-8')

        # Checking if recipe exists
        self.assertIn(needed_title, content)

    def test_receita_detail_template_loads_the_correct_receita(self):
        needed_title = 'This is a detail page - It loads one recipe'

        self.make_receita(title=needed_title)

        response = self.client.get(
            reverse(
                'receitas:receita',
                kwargs={
                    'pk': 1
                }
            )
        )
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_receita_category_template_dont_load_receitas_not_published(self):
        receita = self.make_receita(is_published=False)

        response = self.client.get(
            reverse('receitas:receita', kwargs={'pk': receita.category.pk})
        )

        self.assertEqual(response.status_code, 404)

    def test_receita_detail_template_dont_load_receita_not_published(self):
        receita = self.make_receita(is_published=False)

        response = self.client.get(
            reverse(
                'receitas:receita',
                kwargs={
                    'pk': receita.pk
                }
            )
        )

        self.assertEqual(response.status_code, 404)

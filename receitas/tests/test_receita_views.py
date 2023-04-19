from django.test import TestCase
from django.urls import resolve, reverse

from receitas.views import (RecipeDetail, RecipeListViewCategory,
                            RecipeListViewHome, RecipeListViewSearch)


class ReceitaViewsTest(TestCase):

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

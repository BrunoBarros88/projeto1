from django.test import TestCase
from django.urls import reverse


class receitaURLsTest(TestCase):
    def test_receita_home_url_is_correct(self):
        home_url = reverse('receitas:home')
        self.assertEqual(home_url, '/')

    def test_receita_category_url_is_correct(self):
        url = reverse('receitas:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/receita/category/1')

    def test_receita_detail_url_is_correct(self):
        url = reverse('receitas:receita', kwargs={'pk': 1})
        self.assertEqual(url, '/receita/1')

    def test_receita_search_url_is_correct(self):
        url = reverse('receitas:search')
        self.assertEqual(url, '/receita/search/')

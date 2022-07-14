from django.test import TestCase
from django.urls import reverse


class receitaURLsTest(TestCase):
    def test_receita_home_url_is_correct(self):
        url = reverse('receitas:home')
        self.assertEqual(url, '/')

    def test_receita_category_url_is_correct(self):
        url = reverse('receitas:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/receita/category/1')

    def test_receita_detail_url_is_correct(self):
        url = reverse('receitas:receita', kwargs={'id': 4})
        self.assertEqual(url, '/receita/4')

    def test_receita_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('receitas:home'))
        self.assertEqual(response.status_code, 200)

    def test_receita_home_view_loads_correct_template(self):
        response = self.client.get(reverse('receitas:home'))
        self.assertTemplateUsed(response, 'receitas/home.html')

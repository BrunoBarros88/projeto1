from django.test import TestCase
from django.urls import resolve, reverse
from receitas import views


class receitaViewsTest(TestCase):
    def test_receita_home_view_function_is_correct(self):
        view = resolve(reverse('receitas:home'))
        self.assertIs(view.func, views.home)

    def test_receita_category_view_function_is_correct(self):
        view = resolve(
            reverse('receitas:category', kwargs={'category_id': 1})
        )
        self.assertIs(view.func, views.category)

    def test_receita_detail_view_function_is_correct(self):
        view = resolve(
            reverse('receitas:receita', kwargs={'id': 4})
        )
        self.assertIs(view.func, views.receita)

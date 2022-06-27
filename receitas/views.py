
from django.shortcuts import render
from utils.receitas.factory import make_recipe

from receitas.models import Receita


def home(request):
    receitas = Receita.objects.all().order_by('-id')
    return render(request, 'receitas/home.html', context={'receitas': receitas, })


def category(request, category_id):
    receitas = Receita.objects.filter(category__id=category_id).order_by('-id')
    return render(request, 'receitas/home.html', context={'receitas': receitas, })


def receita(request, id):
    return render(request, 'receitas/receita-view.html', context={'receita': make_recipe(),
                                                                  'is_detail_page': True, })

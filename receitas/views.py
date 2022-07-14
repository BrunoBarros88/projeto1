import os

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from utils.pagination import make_pagination

from receitas.models import Receita

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def home(request):
    receitas = Receita.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(request, receitas, PER_PAGE)
    return render(request, 'receitas/home.html', context={
        'receitas': page_obj,
        'pagination_range': pagination_range
    })


def category(request, category_id):
    receitas = Receita.objects.filter(
        category__id=category_id, is_published=True).order_by('-id')
    if not receitas:
        raise Http404('Not found :( ')
    page_obj, pagination_range = make_pagination(request, receitas, PER_PAGE)
    return render(request, 'receitas/home.html', context={'receitas': page_obj, 'pagination_range': pagination_range, 'title': f'{receitas.first().category.name}'})


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()
    receitas = Receita.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True,
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, receitas, PER_PAGE)

    return render(request, 'receitas/search.html', {'page_title': f'Search for "{search_term}" |',
                                                    'search_term': search_term, 'receitas': page_obj, 'pagination_range': pagination_range,
                                                    'additional_url_query': f'&q={search_term}', })


def receita(request, id):
    receita = Receita.objects.filter(
        pk=id,
        is_published=True,
    ).order_by('-id').first()
    return render(request, 'receitas/receita-view.html', context={'receita': receita,
                                                                  'is_detail_page': True, })

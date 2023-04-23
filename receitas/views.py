import os

from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
from django.views.generic import DetailView, ListView

from receitas.models import Receita
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Receita
    context_object_name = 'receitas'
    ordering = ['-id']
    template_name = 'receitas/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        qs = qs.select_related('author', 'category', )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('receitas'),
            PER_PAGE
        )
        ctx.update(
            {'receitas': page_obj, 'pagination_range': pagination_range}
        )
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'receitas/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'receitas/home.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'title': f'{ctx.get("receitas")[0].category.name} - Category | '
        })

        return ctx

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(category__id=self.kwargs.get('category_id'),

                       )
        if not qs:
            raise Http404()

        return qs


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'receitas/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return ctx


class RecipeDetail(DetailView):
    model = Receita
    context_object_name = 'receita'
    template_name = 'receitas/receita-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update(
            {'is_detail_page': True}
        )
        return ctx


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'receitas/home.html'

    def render_to_response(self, context, **response_kwargs):
        receitas = self.get_context_data()['receitas']
        receitas_list = receitas.object_list.values()

        return JsonResponse(
            list(receitas_list),
            safe=False
        )


class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        receita = self.get_context_data()['receita']
        receita_dict = model_to_dict(receita)

        receita_dict['created_at'] = str(receita.created_at)
        receita_dict['updated_at'] = str(receita.updated_at)

        if receita_dict.get('cover'):
            receita_dict['cover'] = self.request.build_absolute_uri() + \
                receita_dict['cover'].url[1:]
        else:
            receita_dict['cover'] = ''

        del receita_dict['is_published']
        del receita_dict['preparation_steps_is_html']

        return JsonResponse(
            receita_dict,
            safe=False,
        )

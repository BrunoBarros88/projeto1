from django.contrib import admin

# Register your models here.
from .models import Category, Receita


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_published', 'author']
    list_display_links = 'title', 'created_at',
    search_fields = 'id', 'title', 'description', 'slug', 'preparation_steps',
    list_filter = 'category', 'author', 'is_published',\
        'preparation_steps_is_html',
    list_per_page = 15
    list_editable = 'is_published',
    prepopulated_fields = {
        "slug": ('title',)
    }


admin.site.register(Category, CategoryAdmin)

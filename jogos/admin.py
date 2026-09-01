from django.contrib import admin
from .models import Categoria, Plataforma, Jogo

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Plataforma)
class PlataformaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'tipo_midia', 'estoque')
    search_fields = ('nome', 'categorias__nome', 'plataformas__nome')
    filter_horizontal = ('categorias', 'plataformas')
    list_filter = ('tipo_midia', 'categorias', 'plataformas')
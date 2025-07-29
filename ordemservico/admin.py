from django.contrib import admin
from .models import Categoria, OrdemServico, Servico, FotoServico


class FotoServicoInline(admin.TabularInline):
    model = FotoServico
    extra = 1


class ServicoInline(admin.StackedInline):
    model = Servico
    extra = 1
    inlines = [FotoServicoInline]


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")
    search_fields = ("nome",)


@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'contrato', 'local', 'situacao', 'data_inicio', 'data_termino')
    list_filter = ('situacao', 'data_inicio', 'local')
    search_fields = ('numero', 'contrato__numero', 'local__nome')
    autocomplete_fields = ['contrato', 'local']


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ("descricao", "ordem", "situacao", "quantidade", "categoria")
    list_filter = ("situacao", "categoria")
    search_fields = ("descricao", "ordem__numero")


@admin.register(FotoServico)
class FotoServicoAdmin(admin.ModelAdmin):
    list_display = ("servico", "imagem")

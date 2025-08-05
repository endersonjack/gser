from django.contrib import admin
from .models import Categoria, OrdemServico, Servico, Album, Foto

# FOTO Inline dentro do Álbum
class FotoInline(admin.TabularInline):
    model = Foto
    extra = 1

# Álbum Admin com suas fotos
@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('nome', 'servico', 'criado_em')
    search_fields = ('nome', 'servico__descricao')
    list_filter = ('criado_em',)
    inlines = [FotoInline]

# Foto Admin direto (caso queira ver individualmente)
@admin.register(Foto)
class FotoAdmin(admin.ModelAdmin):
    list_display = ('album', 'legenda', 'criado_em')
    list_filter = ('album',)
    search_fields = ('legenda', 'album__nome')

# Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")
    search_fields = ("nome",)

# Ordem de Serviço
@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'contrato', 'local', 'situacao', 'data_inicio', 'data_termino')
    list_filter = ('situacao', 'data_inicio', 'local')
    search_fields = ('numero', 'contrato__numero', 'local__nome')
    autocomplete_fields = ['contrato', 'local']

# Serviço
@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ("descricao", "ordem", "situacao", "quantidade", "categoria")
    list_filter = ("situacao", "categoria")
    search_fields = ("descricao", "ordem__numero")

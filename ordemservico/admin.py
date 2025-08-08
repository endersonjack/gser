from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, OrdemServico, Servico, Album, Foto


# =========================
# INLINES
# =========================
class FotoInline(admin.TabularInline):
    model = Foto
    extra = 1


class ServicoInline(admin.TabularInline):
    model = Servico
    extra = 0
    fields = ("descricao", "situacao", "quantidade", "categoria", "observacao")
    show_change_link = True


# =========================
# ÁLBUM / FOTO
# =========================
@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("nome", "servico", "criado_em")
    search_fields = ("nome", "servico__descricao")
    list_filter = ("criado_em",)
    inlines = [FotoInline]


@admin.register(Foto)
class FotoAdmin(admin.ModelAdmin):
    list_display = ("album", "legenda", "criado_em")
    list_filter = ("album",)
    search_fields = ("legenda", "album__nome")


# =========================
# CATEGORIA
# =========================
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")
    search_fields = ("nome",)
    ordering = ("nome",)


# =========================
# ORDEM DE SERVIÇO
# =========================
@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    # Colunas
    list_display = (
        "num_formatado", "contrato", "local", "situacao",
        "urgente", "data_inicio", "data_termino",
    )
    list_display_links = ("num_formatado",)
    list_editable = ("urgente",)  # permite marcar/desmarcar direto na lista

    # Filtros e busca
    list_filter = ("urgente", "situacao", "data_inicio", "local")
    search_fields = ("numero", "contrato__numero", "local__nome")
    autocomplete_fields = ["contrato", "local"]

    # Inline de serviços para visão rápida
    inlines = [ServicoInline]

    # Qualidade de vida
    date_hierarchy = "data_inicio"
    ordering = ("-urgente", "situacao", "data_inicio")
    list_per_page = 25

    # Ações em massa
    @admin.action(description="Marcar selecionadas como URGENTES")
    def marcar_urgente(self, request, queryset):
        queryset.update(urgente=True)

    @admin.action(description="Desmarcar URGÊNCIA das selecionadas")
    def desmarcar_urgente(self, request, queryset):
        queryset.update(urgente=False)

    actions = ["marcar_urgente", "desmarcar_urgente"]

    # Exibição do número formatado (0001, 0002...)
    @admin.display(ordering="numero", description="Nº OS")
    def num_formatado(self, obj):
        return obj.numero_formatado


# =========================
# SERVIÇO
# =========================
@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ("descricao_curta", "ordem", "situacao", "quantidade", "categoria")
    list_filter = ("situacao", "categoria")
    search_fields = ("descricao", "ordem__numero", "ordem__contrato__numero")
    autocomplete_fields = ["ordem", "categoria"]
    list_select_related = ("ordem", "categoria")

    @admin.display(description="Descrição")
    def descricao_curta(self, obj):
        txt = (obj.descricao or "").strip()
        return txt if len(txt) <= 60 else f"{txt[:60]}..."

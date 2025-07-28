from django.contrib import admin
from .models import Contrato

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = (
        'numero', 
        'empresa_contratada', 
        'orgao_contratante', 
        'valor_total', 
        'status', 
        'data_inicio', 
        'data_fim'
    )
    search_fields = ('numero', 'empresa_contratada', 'orgao_contratante')
    list_filter = ('status', 'data_inicio', 'data_fim')

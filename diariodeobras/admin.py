from django.contrib import admin
from .models import Orgao

@admin.register(Orgao)
class OrgaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "prefeitura", "departamento")
    search_fields = ("nome", "prefeitura", "departamento", "endereco")

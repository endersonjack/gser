from django.contrib import admin

# Register your models here.
from .models import Empresa

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("nome", "cnpj", "telefone")
    search_fields = ("nome", "cnpj")
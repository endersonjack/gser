from django.db import models

# Create your models here.
class Empresa(models.Model):
    nome = models.CharField("Nome da Empresa", max_length=255)
    cnpj = models.CharField("CNPJ", max_length=18, unique=True)
    logo = models.ImageField("Logo", upload_to="empresas/logos/", blank=True, null=True)
    endereco = models.CharField("Endereço", max_length=255, blank=True, null=True)
    telefone = models.CharField("Telefone", max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nome
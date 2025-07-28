from django.db import models

# Create your models here.
class Local(models.Model):
    nome = models.CharField("Nome do Local", max_length=200)
    endereco = models.TextField("Endereço")

    def __str__(self):
        return self.nome
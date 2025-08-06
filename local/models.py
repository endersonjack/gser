from django.db import models
import re

# Create your models here.
class Local(models.Model):
    nome = models.CharField("Nome do Local", max_length=200)
    endereco = models.TextField("Endereço", blank=True, null=True)
    link_maps = models.URLField("Link do Google Maps", blank=True, null=True)
    latitude = models.FloatField("Latitude", blank=True, null=True)
    longitude = models.FloatField("Longitude", blank=True, null=True)

    def __str__(self):
        return self.nome
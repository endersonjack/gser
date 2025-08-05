from django.db import models
from contratos.models import Contrato
from local.models import Local


class Categoria(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome


class OrdemServico(models.Model):
    STATUS_CHOICES = [
        ("nao_iniciado", "Não Iniciado"),
        ("em_andamento", "Em Andamento"),
        ("pendente", "Pendente"),
        ("paralisado", "Paralisado"),
        ("cancelado", "Cancelado"),
        ("finalizado", "Finalizado"),
    ]

    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='ordens')
    numero = models.CharField(max_length=50)
    local = models.ForeignKey(Local, on_delete=models.SET_NULL, null=True, blank=True)  
    data_inicio = models.DateField()
    data_termino = models.DateField(null=True, blank=True)
    data_paralisado = models.DateField(null=True, blank=True)
    motivo_pendente_paralisado = models.TextField(blank=True)
    situacao = models.CharField(max_length=20, choices=STATUS_CHOICES)
    observacao = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.situacao not in ['pendente', 'paralisado']:
            self.motivo_pendente_paralisado = ''
            self.data_paralisado = None

        if self.situacao != 'finalizado':
            self.data_termino = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"OS {self.numero} - Contrato {self.contrato.numero}"
    
    #o sistema permitirá números repetidos em contratos diferentes, mas bloqueará repetições no mesmo contrato.
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['contrato', 'numero'], name='unique_numero_por_contrato')
        ]



class Servico(models.Model):
    ordem = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='servicos')
    descricao = models.TextField()
    situacao = models.CharField(max_length=20, choices=OrdemServico.STATUS_CHOICES)
    quantidade = models.TextField(null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    observacao = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.descricao[:40]}..."


class Album(models.Model):
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name="albuns")
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Foto(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="fotos")
    imagem = models.ImageField(upload_to="fotos_servico/")
    legenda = models.CharField(max_length=255, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Foto de {self.album.nome}"

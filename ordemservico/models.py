from django.db import models
from contratos.models import Contrato
from local.models import Local
from django.utils.timezone import now


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
    data_solicitacao = models.DateField("Data da Solicitação", default=now)
    data_inicio = models.DateField()
    data_termino = models.DateField(null=True, blank=True)
    data_paralisado = models.DateField(null=True, blank=True)
    motivo_pendente_paralisado = models.TextField(blank=True)
    situacao = models.CharField(max_length=20, choices=STATUS_CHOICES)
    observacao = models.TextField(blank=True)

    # Campo simples para marcar urgência
    urgente = models.BooleanField(default=False, verbose_name="Urgente")

    def save(self, *args, **kwargs):
        # limpeza dos campos já existente
        if self.situacao not in ['pendente', 'paralisado']:
            self.motivo_pendente_paralisado = ''
            self.data_paralisado = None
        if self.situacao != 'finalizado':
            self.data_termino = None

        # Se finalizou, não pode permanecer urgente
        if self.situacao == 'finalizado' and self.urgente:
            self.urgente = False

        # Flags para pós-save
        finalizando = (self.situacao == 'finalizado')

        # descobrir valor anterior de 'urgente' (para saber se acabou de ligar)
        was_urgent = None
        if self.pk:
            was_urgent = type(self).objects.filter(pk=self.pk).values_list('urgente', flat=True).first()

        super().save(*args, **kwargs)

        # Se a OS acabou de virar urgente (e não está finalizada), propaga para serviços existentes
        if self.urgente and (was_urgent is False or was_urgent is None) and not finalizando:
            # bulk update, sem disparar save() por item (rápido)
            self.servicos.update(urgente=True)

        # Se finalizou, zera urgência de todos os serviços
        if finalizando:
            self.servicos.filter(urgente=True).update(urgente=False)


class Servico(models.Model):
    ordem = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='servicos')
    descricao = models.TextField()
    situacao = models.CharField(max_length=20, choices=OrdemServico.STATUS_CHOICES)
    quantidade = models.TextField(null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    observacao = models.TextField(null=True, blank=True)
    prazo_entrega = models.DateField("Prazo de Entrega", null=True, blank=True)
    data_finalizacao = models.DateField("Data de Finalização", null=True, blank=True)
    urgente = models.BooleanField(default=False, verbose_name="Urgente")

    def save(self, *args, **kwargs):
        # Se não estiver finalizado, não guarda data_finalizacao
        if self.situacao != 'finalizado':
            self.data_finalizacao = None

        # Se a OS está finalizada, o serviço não pode permanecer urgente
        if self.ordem_id and self.ordem.situacao == 'finalizado' and self.urgente:
            self.urgente = False

        was_urgent = None
        if self.pk:
            was_urgent = type(self).objects.filter(pk=self.pk).values_list('urgente', flat=True).first()

        super().save(*args, **kwargs)

        # Se o serviço virou urgente agora, só "sobe" para a OS se a OS não estiver finalizada
        if self.urgente and (was_urgent is False or was_urgent is None):
            if not self.ordem.urgente and self.ordem.situacao != 'finalizado':
                # evita religar urgência em OS finalizada
                OrdemServico.objects.filter(pk=self.ordem_id).exclude(situacao='finalizado').update(urgente=True)

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

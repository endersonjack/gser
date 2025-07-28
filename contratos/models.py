from django.db import models


class Contrato(models.Model):
    numero = models.CharField("Nº do Contrato", max_length=50, unique=True)
    objeto = models.TextField("Objeto do Contrato")
    empresa_contratada = models.CharField("Empresa Contratada", max_length=200)
    cnpj = models.CharField("CNPJ", max_length=18)
    valor_total = models.DecimalField("Valor Total", max_digits=12, decimal_places=2)
    data_inicio = models.DateField("Data de Início")
    data_fim = models.DateField("Data de Término")
    orgao_contratante = models.CharField("Órgão Público Contratante", max_length=200)
    fiscal = models.CharField("Fiscal do Contrato", max_length=100)
    status = models.CharField(
        "Status",
        max_length=20,
        choices=[
            ('vigente', 'Vigente'),
            ('encerrado', 'Encerrado'),
            ('rescindido', 'Rescindido'),
            ('suspenso', 'Suspenso'),
        ],
        default='vigente'
    )
    observacoes = models.TextField("Observações", blank=True, null=True)

    def __str__(self):
        return f"{self.numero} - {self.empresa_contratada}"
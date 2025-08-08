from django.db import models

class Orgao(models.Model):
    nome = models.CharField("Nome", max_length=150)
    prefeitura = models.CharField("Prefeitura", max_length=150)
    departamento = models.CharField("Departamento", max_length=150, blank=True)

    endereco = models.CharField("Endereço", max_length=255, blank=True)

    logo = models.ImageField("Logo", upload_to="orgaos/%Y/%m/", blank=True, null=True)

    assinatura_fiscal = models.ImageField(
        "Assinatura Fiscal", upload_to="orgaos/assinaturas/%Y/%m/", blank=True, null=True
    )
    assinatura_engenheiro = models.ImageField(
        "Assinatura Engenheiro", upload_to="orgaos/assinaturas/%Y/%m/", blank=True, null=True
    )
    assinatura_gestor = models.ImageField(
        "Assinatura Gestor", upload_to="orgaos/assinaturas/%Y/%m/", blank=True, null=True
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Órgão"
        verbose_name_plural = "Órgãos"
        ordering = ["prefeitura", "departamento", "nome"]

    def __str__(self):
        base = self.nome or self.prefeitura
        if self.departamento:
            base += f" — {self.departamento}"
        return base

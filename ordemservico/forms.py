from django import forms
from django.forms import inlineformset_factory
from django.forms.widgets import ClearableFileInput
from .models import OrdemServico, Servico, Categoria, Album, Foto, Local
from django.utils import timezone


# -------------------------
# ORDEM DE SERVIÇO
# -------------------------

class OrdemServicoForm(forms.ModelForm):
    # Força widget no formato ISO e inicial = hoje
    data_solicitacao = forms.DateField(
        label="Data da Solicitação",
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"type": "date", "class": "form-control"}
        ),
        input_formats=["%Y-%m-%d"],
        initial=timezone.localdate,   # hoje
        required=True,
    )

    class Meta:
        model = OrdemServico
        fields = [
            "numero", "local", "contrato",
            "data_solicitacao",
            "data_inicio", "data_termino", "data_paralisado",
            "motivo_pendente_paralisado", "situacao", "observacao", "urgente",
        ]
        widgets = {
            "contrato": forms.Select(attrs={"class": "form-select"}),
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "local": forms.Select(attrs={"class": "form-select select2"}),
            "situacao": forms.Select(attrs={"class": "form-select"}),
            "data_inicio": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
            "data_termino": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
            "data_paralisado": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
            "motivo_pendente_paralisado": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "observacao": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "urgente": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["local"].queryset = Local.objects.order_by("nome")
        # Se for NOVO (GET, não-bound e sem instance), garante value no HTML
        if not self.is_bound and not (self.instance and self.instance.pk):
            today = timezone.localdate()
            self.initial.setdefault("data_solicitacao", today)
            self.fields["data_solicitacao"].widget.attrs["value"] = today.isoformat()

class OrdemServicoEditForm(forms.ModelForm):
    # Mesmo widget/format para edição (sem initial)
    data_solicitacao = forms.DateField(
        label="Data da Solicitação",
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"type": "date", "class": "form-control"}
        ),
        input_formats=["%Y-%m-%d"],
        required=True,
    )

    class Meta:
        model = OrdemServico
        fields = [
            "numero", "contrato", "local",
            "data_solicitacao",
            "data_inicio", "data_termino", "data_paralisado",
            "motivo_pendente_paralisado", "situacao", "observacao", "urgente",
        ]
        widgets = {
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "contrato": forms.Select(attrs={"class": "form-select", "disabled": "disabled"}),
            "local": forms.Select(attrs={"class": "form-select"}),
            "situacao": forms.Select(attrs={"class": "form-select"}),
            "data_inicio": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
            "data_termino": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
            "data_paralisado": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
            "motivo_pendente_paralisado": forms.Textarea(attrs={"rows": 1, "class": "form-control"}),
            "observacao": forms.Textarea(attrs={"rows": 1, "class": "form-control"}),
            "urgente": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["local"].queryset = Local.objects.order_by("nome")
        if self.instance and self.instance.pk:
            self.fields["contrato"].initial = self.instance.contrato


# -------------------------
# SERVIÇO
# -------------------------
class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = [
            'descricao', 'situacao', 'quantidade',
            'categoria', 'observacao',
            'prazo_entrega', 'data_finalizacao',   # <-- NOVOS
            'urgente'                              # <-- útil já no cadastro do serviço
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 1, 'class': 'form-control', 'placeholder': 'Descreva o serviço...'}),
            'situacao': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),  # aceita parágrafos
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'observacao': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),

            'prazo_entrega': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),   # <-- NOVO
            'data_finalizacao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),# <-- NOVO
            'urgente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'prazo_entrega': 'Prazo de Entrega',
            'data_finalizacao': 'Data de Finalização',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Evita que "None" apareça no campo de texto
        if self.instance and self.instance.quantidade is None:
            self.initial['quantidade'] = ''
        # Ordena categorias alfabeticamente
        self.fields['categoria'].queryset = Categoria.objects.order_by('nome')


# -------------------------
# CATEGORIA
# -------------------------
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# -------------------------
# FORMSET DE SERVIÇOS INLINE
# -------------------------
ServicoFormSet = inlineformset_factory(
    parent_model=OrdemServico,
    model=Servico,
    fields=[
        'descricao', 'situacao', 'quantidade', 'categoria', 'observacao',
        'prazo_entrega', 'data_finalizacao', 'urgente'   # <-- NOVOS
    ],
    widgets={
        'descricao': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        'situacao': forms.Select(attrs={'class': 'form-select'}),
        'quantidade': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        'categoria': forms.Select(attrs={'class': 'form-select'}),
        'observacao': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),

        'prazo_entrega': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),   # <-- NOVO
        'data_finalizacao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),# <-- NOVO
        'urgente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    },
    extra=1,
    can_delete=True
)


# -------------------------
# ÁLBUM / FOTOS
# -------------------------
class MultiFileInput(ClearableFileInput):
    allow_multiple_selected = True


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['nome', 'descricao']


class FotoForm(forms.ModelForm):
    class Meta:
        model = Foto
        fields = ['imagem', 'legenda']

    # permite múltiplos arquivos na mesma seleção
    imagem = forms.ImageField(widget=MultiFileInput(attrs={'multiple': True}))

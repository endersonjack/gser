from django import forms
from django.forms import inlineformset_factory
from django.forms.widgets import ClearableFileInput
from .models import OrdemServico, Servico, Categoria, Album, Foto, Local


# -------------------------
# ORDEM DE SERVIÇO
# -------------------------
class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = [
            'numero', 'local', 'contrato', 'data_inicio', 'data_termino', 'data_paralisado',
            'motivo_pendente_paralisado', 'situacao', 'observacao', 'urgente'
        ]
        widgets = {
            'contrato': forms.Select(attrs={'class': 'form-select'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'local': forms.Select(attrs={'class': 'form-select'}),
            'situacao': forms.Select(attrs={'class': 'form-select'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_termino': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_paralisado': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'motivo_pendente_paralisado': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'urgente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'urgente': 'Urgente',
        }
        help_texts = {
            'urgente': 'Marque para destacar esta OS como urgente.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenações
        self.fields['local'].queryset = Local.objects.order_by('nome')


class OrdemServicoEditForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = [
            'numero', 'contrato', 'local', 'data_inicio',
            'data_termino', 'data_paralisado',
            'motivo_pendente_paralisado', 'situacao', 'observacao', 'urgente'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'contrato': forms.Select(attrs={'class': 'form-select', 'disabled': 'disabled'}),  # visível, porém desabilitado
            'local': forms.Select(attrs={'class': 'form-select'}),
            'situacao': forms.Select(attrs={'class': 'form-select'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_termino': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_paralisado': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'motivo_pendente_paralisado': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
            'urgente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'urgente': 'Urgente',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['local'].queryset = Local.objects.order_by('nome')

        # Importante: como 'contrato' está desabilitado (disabled), o browser não envia o valor.
        # Garantimos o valor original da instância para não perder o vínculo ao salvar.
        if self.instance and self.instance.pk:
            self.fields['contrato'].initial = self.instance.contrato

    def clean_contrato(self):
        # Mantém o contrato original quando o campo está desabilitado no form
        if self.instance and self.instance.pk:
            return self.instance.contrato
        return self.cleaned_data.get('contrato')


# -------------------------
# SERVIÇO
# -------------------------
class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['descricao', 'situacao', 'quantidade', 'categoria', 'observacao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 1, 'class': 'form-control', 'placeholder': 'Descreva o serviço...'}),
            'situacao': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),  # aceita parágrafos
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'observacao': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
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
    fields=['descricao', 'situacao', 'quantidade', 'categoria', 'observacao'],
    widgets={
        'descricao': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        'situacao': forms.Select(attrs={'class': 'form-select'}),
        'quantidade': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        'categoria': forms.Select(attrs={'class': 'form-select'}),
        'observacao': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
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

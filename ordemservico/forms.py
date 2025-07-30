from django import forms
from django.forms import inlineformset_factory
from .models import OrdemServico, Servico, Categoria

class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = ['numero', 'local', 'data_inicio', 'data_termino', 'data_paralisado',
                  'motivo_pendente_paralisado', 'situacao', 'observacao']
        widgets = {
            # 'contrato': forms.Select(attrs={'class': 'form-select'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'local': forms.Select(attrs={'class': 'form-select'}),
            'situacao': forms.Select(attrs={'class': 'form-select'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_termino': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_paralisado': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'motivo_pendente_paralisado': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

class OrdemServicoEditForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = [
            'numero', 'contrato', 'local', 'data_inicio',
            'data_termino', 'data_paralisado',
            'motivo_pendente_paralisado', 'situacao', 'observacao'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'contrato': forms.Select(attrs={'class': 'form-select'}),  # <- ADICIONADO
            'local': forms.Select(attrs={'class': 'form-select'}),
            'situacao': forms.Select(attrs={'class': 'form-select'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_termino': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_paralisado': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'motivo_pendente_paralisado': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
        }




class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['descricao', 'situacao', 'quantidade', 'categoria', 'observacao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
            'situacao': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),  # ← AQUI!
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'observacao': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Evita que "None" apareça no campo de texto
        if self.instance and self.instance.quantidade is None:
            self.initial['quantidade'] = ''

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Formset para Serviços Inline

ServicoFormSet = inlineformset_factory(
    parent_model=OrdemServico,
    model=Servico,
    fields=['descricao', 'situacao', 'quantidade', 'categoria', 'observacao'],
    widgets={
        'descricao': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        'observacao': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
    },
    extra=1,
    can_delete=True
)
from django import forms
from .models import Setor, Colaborador, Tarefa

# ==============================
# FORM DE SETOR
# ==============================
class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = [
            'nome',
            'descricao',
            'imagem',
            'dimensao',
            'natureza_piso',
            'area_envidracada',
            'mobilia',
        ]


# ==============================
# FORM DE COLABORADOR
# ==============================
class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = '__all__'

        
        widgets = {
            'data_admissao': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }


# ==============================
# FORM DE TAREFA
# ==============================
class TarefaForm(forms.ModelForm):

    setores = forms.ModelMultipleChoiceField(
        queryset=Setor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    colaboradores = forms.ModelMultipleChoiceField(
        queryset=Colaborador.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


    class Meta:
        model = Tarefa
        fields = '__all__'
        exclude = ['setores','colaboradores']

        widgets = {
            'data_inicio': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'data_previsao_termino': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'data_termino': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in [
            'data_inicio',
            'data_previsao_termino',
            'data_termino'
        ]:
            self.fields[field].input_formats = ['%Y-%m-%dT%H:%M']
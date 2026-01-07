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


# ==============================
# FORM DE TAREFA
# ==============================
class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = '__all__'

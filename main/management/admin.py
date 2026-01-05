from django.contrib import admin
from .models import Colaborador, Setor, Tarefa, TarefaColaborador, TarefaSetor

@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'status', 'telefone', 'numero_empresa', 'data_admissao')
    search_fields = ('nome', 'telefone')
    list_filter = ('status',)

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'dimensao', 'mobilia', 'natureza_piso')
    search_fields = ('nome', 'descricao')
    list_filter = ('mobilia', 'natureza_piso')

class TarefaColaboradorInline(admin.TabularInline):
    model = TarefaColaborador
    extra = 1

class TarefaSetorInline(admin.TabularInline):
    model = TarefaSetor
    extra = 1

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'status',
        'prioridade',
        'nivel_sujeira',
        'data_inicio',
        'data_previsao_termino',
        'data_termino',
    )

    list_filter = (
        'status',
        'prioridade',
        'nivel_sujeira',
        'data_inicio',
    )

    search_fields = ('titulo', 'descricao')

    inlines = [TarefaColaboradorInline, TarefaSetorInline]

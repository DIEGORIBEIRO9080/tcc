from django.urls import path
from management.views import *

app_name = 'management'

urlpatterns = [
    path('', home),
    

    path('usuarios/', lista_usuarios, name='lista_usuarios'),
    
    ##############################################################################
    ####################             SETORES        ##############################
    ##############################################################################
    path('setores/', sectors, name='sectors'),
    path('setores/create/', setor_create, name='setor_create'),
    path('setores/<str:id>/editar/', setor_edit, name='setor_edit'),


    ##############################################################################
    ####################         COLABORADORES      ##############################
    ##############################################################################
    path('colaboradores/', colaborators,  name='colaborators' ),
    path('colaboradores/create/', colaborador_create, name='colaborador_create'),
    path('colaboradores/<str:id>/editar/', colaborador_edit, name='colaborador_edit'),

    ##############################################################################
    ####################             TAREFAS        ##############################
    ##############################################################################
    path('tarefas/', tasks, name='tasks' ),
    path('tarefas/create/', tarefa_create, name='tarefa_create'),
    path('tarefas/<str:id>/editar/', tarefa_edit, name='tarefa_edit'),


]
from django.urls import path
from management.views import *
from . import views
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
    path('setores/delete/<str:id>/', views.setor_delete, name='setor_delete'),





    ##############################################################################
    ####################         COLABORADORES      ##############################
    ##############################################################################
    path('colaboradores/', colaborators,  name='colaborators' ),
    path('colaboradores/create/', colaborador_create, name='colaborador_create'),
    path('colaboradores/<str:id>/editar/', colaborador_edit, name='colaborador_edit'),
    path('colaboradores/<str:id>/status/<str:novo_status>/',colaborador_mudar_status,name='colaborador_mudar_status'),
    path('colaboradores/delete/<str:id>/', views.colaborador_delete, name='colaborador_delete'),


    ##############################################################################
    ####################             TAREFAS        ##############################
    ##############################################################################
    path('tarefas/', tasks, name='tasks' ),
    path('tarefas/create/', tarefa_create, name='tarefa_create'),
    path('tarefas/<str:id>/editar/', tarefa_edit, name='tarefa_edit'),
    path('tarefas/<str:tarefa_id>/status/<str:novo_status>/',alterar_status_tarefa,name='alterar_status_tarefa'),
    path('tarefas/delete/<str:id>/', views.tarefa_delete, name='tarefa_delete'),

    ##############################################################################
    ####################           reelatorios      ##############################
    ##############################################################################

    path('relatorios/menu', views.relatorio_menu, name='relatorio_menu' ),
    path('relatorios/', views.relatorio_form, name='relatorio_form'),
    path('relatorios/gerar/', views.gerar_relatorio, name='gerar_relatorio'),
    path('relatorios/dashboard/', views.dashboard_relatorios, name='dashboard_relatorios'),
    path('relatorios/dashboard/menu', views.dashboard_menu, name='dashboard_menu'),
    path('relatorios/dashboard/dados/', views.dashboard_relatorios, name='dashboard_relatorios'),

    path('notificacoes/', notificacoes_tarefas, name='notificacoes_tarefas'),

    ##############################################################################
    ####################          CONFIGURAÇÃO      ##############################
    ##############################################################################

    path("configuracoes/", views.configuracoes_view, name="configuracoes"),
]
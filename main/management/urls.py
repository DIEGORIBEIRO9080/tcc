from django.urls import path
from management.views import *

urlpatterns = [
    path('', home),
    path('setores/', sectors),
    path('colaboradores/', colaborators ),
    path('tarefas/', tasks ),
    path('usuarios/', lista_usuarios, name='lista_usuarios'),
]
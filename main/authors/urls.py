from django.urls import path
from authors.views import *

app_name = 'authors' 

urlpatterns = [
    path('cadastrar/', register_view , name='usuarios_cadastrar'),

]
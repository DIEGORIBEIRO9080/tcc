from django.urls import path
from authors.views import *
from . import views
app_name = 'authors' 

urlpatterns = [
    path('cadastrar/', register_view , name='usuarios_cadastrar'),
    path('create/', register_create , name='create'),
    
    path("usuarios/<int:user_id>/editar/", views.user_edit_view, name="user_edit"),
    path("usuarios/<int:user_id>/editar/salvar/", views.user_edit_save, name="user_edit_save"),
    path('delete/<int:id>/', views.user_delete, name='user_delete'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
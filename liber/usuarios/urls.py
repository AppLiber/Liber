from django.urls import path, re_path

from .views import *

app_name = 'usuarios'
urlpatterns = [
    re_path(r'^cadastrar/$', cadastrar_usuario, name='cadastrar_usuario'),
    re_path(r'^listar/$', listar_usuario, name="listar_usuario"),
    re_path(r'^editar_usuario/(?P<pk>[0-9]+)', editar_usuario, name="editar_usuario"),
    re_path(r'^remover_usuario/(?P<pk>[0-9]+)', remover_usuario, name="remover_usuario"),
    #path('', views.IndexView.as_view(), name='index'),
    #path('<int:pk>/', views.DetailView.as_view(), name='perfil')
]

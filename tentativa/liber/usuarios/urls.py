from django.urls import path, include

# Django local
from . import views

app_name = 'usuarios'
urlpatterns = [
    path('', views.UsuarioIndex.as_view(), name='usuarios_index'),
    path('<int:pk>/', views.UsuarioDetail.as_view(), name='usuarios_detail'),
    path('new', views.UsuarioCreate.as_view(), name='usuarios_new'),
    path('<int:pk>/edit', views.UsuarioUpdate.as_view(), name='usuarios_edit'),
    path('<int:pk>/delete', views.UsuarioDelete.as_view(), name='usuarios_delete'),
]

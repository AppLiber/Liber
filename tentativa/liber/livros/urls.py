from django.urls import path, include

# Django local
from . import views

app_name = 'livros'
urlpatterns = [
    path('', views.LivroIndex.as_view(), name='livros_index'),
    path('<int:pk>/', views.LivroDetail.as_view(), name='livros_detail'),
    path('new', views.LivroCreate.as_view(), name='livros_new'),
    path('<int:pk>/edit', views.LivroUpdate.as_view(), name='livros_edit'),
]

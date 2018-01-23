from django.urls import path
#from .views import *

from . import views

app_name = 'livros'
urlpatterns = [
    path('', views.LivroIndex.as_view(), name='index'),
    path('<int:pk>/', views.LivroDetail.as_view(), name='detalhar_livro'),
    path('new', views.LivroCreate.as_view(), name='livros_new'),
    #path('<int:pk>/edit', views)
    path('<int:pk>/delete', views.LivroDelete.as_view(), name='livros_delete'),
]

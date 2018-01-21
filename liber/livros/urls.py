from django.urls import path
#from .views import *

from . import views

app_name = 'livros'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detalhar_livro'),
]

from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# Django local
from . import views

app_name = 'livros'
urlpatterns = [
    path('', views.LivroIndex.as_view(), name='livros_index'),
    path('<int:pk>/', views.LivroDetail.as_view(), name='livros_detail'),
    path('new', views.LivroCreate.as_view(), name='livros_new'),
    path('<int:pk>/edit', views.LivroUpdate.as_view(), name='livros_edit'),
    path('<int:pk>/delete', views.LivroDelete.as_view(), name='livros_delete'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    path('<int:pk>/adiciona', views.adiciona_livro_na_estante, name='adiciona')
]


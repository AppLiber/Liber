from django.urls import path, include
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.conf.urls.static import static

# Django local
from . import views
from usuarios.views import marcar_livro_lido
#, AvaliaLidoCreate


app_name = 'livros'
urlpatterns = [
    #path('', views.LivroIndex.as_view(), name='livros_index'),
    path('', views.ListLivros.as_view(), name='lista_livros'),
    path('<int:pk>/', views.LivroDetail.as_view(), name='livros_detail'),
    path('<int:pk>/detail', login_required(views.LivroDetailLogado.as_view()), name='livros_detail_logado'),
    path('new', views.LivroCreate.as_view(), name='livros_new'),
    path('autor/new', views.AutorCreate.as_view(), name='autor_new'),
    path('<int:pk>/edit', views.LivroUpdate.as_view(), name='livros_edit'),
    path('<int:pk>/delete', views.LivroDelete.as_view(), name='livros_delete'),
    path('<int:pk>/adiciona', views.adiciona_livro_na_estante, name='adiciona'),
    path('<int:pk>/lido', marcar_livro_lido, name='livrolido'),
    path('<int:pk>/medialivros', views.media_cada_livro, name='medialivros'),
    path('<int:pk>/avalia', views.AvaliaLidoCreate.as_view(), name='avalia_livro'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

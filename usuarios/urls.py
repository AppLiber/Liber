from django.urls import path
from django.contrib.auth.decorators import login_required
# from views import RegistrarUsuarioView

# papra importar imagem
from django.conf import settings
from django.conf.urls.static import static

# Django local
from . import views
from livros.views import apagar_livro_da_estante

app_name = 'usuarios'
urlpatterns = [

    path('', login_required(views.UserIndex.as_view()), name='usuarios_index'),
    path('<int:pk>', views.UserDetail.as_view(), name='home'),
    path('<int:user>/estante', login_required(views.PerfilEstanteList.as_view()), name='estante'),
    path('<int:user>/estante/<int:livro>/apagar', apagar_livro_da_estante, name='apagar_livro' ),
    path('<int:user>/estante/<int:livro>/emprestimo', views.fazer_pedido_de_emprestimo, name='pedir_emprestado'),
    path('<int:user>/avaliacaolivro',(views.LivrosAvaliados.as_view()), name='avaliacaolivro'),
    path('<int:user>/sugestao', views.SugestaoLivro.as_view(), name='sugestao' ),



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

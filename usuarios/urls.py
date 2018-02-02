from django.urls import path
from django.contrib.auth.decorators import login_required
# from views import RegistrarUsuarioView

# papra importar imagem
from django.conf import settings
from django.conf.urls.static import static

# Django local
from . import views

app_name = 'usuarios'
urlpatterns = [

    path('', login_required(views.UserIndex.as_view()), name='usuarios_index'),
    path('<int:pk>', views.UserDetail.as_view(), name='home'),
    path('<int:user>/estante', login_required(views.PerfilEstanteList.as_view()), name='estante'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

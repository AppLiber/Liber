from django.urls import path
from django.contrib.auth.decorators import login_required
# from views import RegistrarUsuarioView


# Django local
from . import views

app_name = 'usuarios'
urlpatterns = [

    path('', login_required(views.UserIndex.as_view()), name='usuarios_index'),
    path('<int:user>/estante', login_required(views.PerfilEstanteList.as_view()), name='estante'),

]

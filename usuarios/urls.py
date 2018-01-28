from django.urls import path
from django.contrib.auth.decorators import login_required
# from views import RegistrarUsuarioView


# Django local
from . import views

app_name = 'usuarios'
urlpatterns = [

    path('', login_required(views.UserIndex.as_view()), name='usuarios_index'),
    #path('login/', views.login , name="cadastrar"),
    #path('login/', 'django.contrib.auth.views.login', name="login"),
    #pathr('logout/', 'django.contrib.auth.views.logout_then_login', name="logout"),

]

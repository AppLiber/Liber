from django.conf.urls import patterns, url
from perfis.views import index
from perfis import views

urlpatterns = patterns('',
    #url(r'^$', views.index, name='index'),
    url(r'^perfis/(?P<perfil_id>)\d+$', views.exibir, name='exibir')
)

from django.conf.urls import patterns, url
from perfis.views import index

urlpatterns = patterns('',
    url(r'^$', index, name='index')
)

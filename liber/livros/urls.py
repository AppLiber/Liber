from django.conf.urls import patterns, url
from livros.views import index
from livros import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^livros/(?P<livro_id>)\d+$', views.detalhar_livro, name='detalhar')
)

from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from .models import Autor, Categoria, Livro
from .forms import LivroForm


class LivroIndex(generic.ListView):
    template_name = 'livros/index.html'
    context_object_name = 'livro_list'

    def get_queryset(self):
        return Livro.objects.all()

class LivroDetail(generic.DetailView):
    model = Livro
    template_name = 'livros/detail.html'

class LivroCreate(generic.CreateView):
    model = Livro
    template_name = 'livros/new.html'
    success_url = reverse_lazy('livros:livros_index')
    form_class = LivroForm

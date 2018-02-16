from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Autor, Categoria, Livro
from usuarios.models import Perfil, Estante, EstanteLivro
from .forms import LivroForm


class LivroIndex(generic.ListView):
    template_name = 'livros/index.html'
    context_object_name = 'livro_list'

    def get_queryset(self):
        return Livro.objects.order_by('titulo')[:4]


class ListLivros(generic.ListView):
    template_name = 'livros/listall.html'
    context_object_name = 'livro_list'

    def get_queryset(self):
        return Livro.objects.order_by('titulo')

class LivroDetail(generic.DetailView):
    model = Livro
    template_name = 'livros/detail.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data()
        #perfil = self.request.user.perfil

        if self.request.user.is_authenticated:
            perfil = get_object_or_404(Perfil, pk=self.request.user.perfil.id)
            livro = Livro.objects.get(pk=self.kwargs['pk'])
            context['estante_livros'] = perfil.estante.estantelivro_set.filter(livro_adicionado=livro)
            context['livros_lidos_total'] = perfil.avalialido_set.all()
            context['livros_lidos'] = perfil.avalialido_set.filter(livro=livro)
            context['medialivros'] = media_cada_livro(self.request, pk=self.kwargs['pk'])




        return context



class LivroCreate(generic.CreateView):
    model = Livro
    template_name = 'livros/new.html'
    success_url = reverse_lazy('livros:livros_index')
    form_class = LivroForm

class LivroUpdate(generic.UpdateView):
    model = Livro
    template_name = 'livros/edit.html'
    form_class = LivroForm

    def get_success_url(self):
        return reverse_lazy('livros:livros_detail', kwargs={'pk':self.kwargs['pk']})

class LivroDelete(generic.DeleteView):
    model = Livro
    success_url = reverse_lazy('livros:livros_index')

@login_required
def adiciona_livro_na_estante(request, pk):

    estante = Estante.objects.get(perfil_dono=request.user.perfil)
    livros_da_estante = estante.livros.all()
    livro = Livro.objects.get(pk=pk)

    if (livro not in livros_da_estante):
        estante.estantelivro_set.create(estante=estante,livro_adicionado=livro)

    return redirect('usuarios:estante', user=request.user.perfil.id)

@login_required
def apagar_livro_da_estante(request, livro, user):

    estante = Estante.objects.get(perfil_dono = request.user.perfil)
    livros_da_estante = estante.livros.all()
    livro = Livro.objects.get(pk=livro)

    #import ipdb; ipdb.set_trace()

    if (livro in livros_da_estante):
        livro_para_apagar = estante.estantelivro_set.get(livro_adicionado=livro)
        livro_para_apagar.delete()

    return redirect('usuarios:estante', user=request.user.perfil.id)


def media_cada_livro(request, pk):

    livroComNotas =  Livro.objects.get(pk=pk)
    notas=livroComNotas.avalialido_set.all()
    somaNotas=0
    medialivros=0
    for nota in notas:
        somaNotas += nota.nota
        medialivros=somaNotas/notas.count()

    return medialivros

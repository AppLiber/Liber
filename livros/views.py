from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Autor, Categoria, Livro
from usuarios.models import Perfil, Estante, EstanteLivro, AvaliaLido, Emprestimo
from usuarios.forms import AvaliaForm, EmprestimoForm , PedirLivroEmprestadoForm
from .forms import LivroForm, AutorForm

import operator

class LivroIndex(generic.ListView):
    template_name = 'livros/index.html'
    context_object_name = 'livro_list'

    def get_queryset(self):
        livros = Livro.objects.all()
        sorted_livro = sorted(livros, key=lambda livro: livro.nota_media())
        sorted_livro.reverse()
        return sorted_livro[:4]


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
        context['medialivros'] = media_cada_livro(self.request, pk=self.kwargs['pk'])
        if self.request.user.is_authenticated:
            perfil = get_object_or_404(Perfil, pk=self.request.user.perfil.id)
            livro = Livro.objects.get(pk=self.kwargs['pk'])
            context['estante_livros'] = perfil.estante.estantelivro_set.filter(livro_adicionado=livro)
            context['livros_lidos_total'] = perfil.avalialido_set.all()
            context['livros_lidos'] = perfil.avalialido_set.filter(livro=livro)


        return context


class LivroDetailLogado(generic.DetailView):
    model = Livro
    template_name = 'livros/detail_logado.html'

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
            context['estantes_com_livro'] = EstanteLivro.objects.filter(livro_adicionado=livro)
            context['form'] = AvaliaForm()
            context['form_emprestimo'] = PedirLivroEmprestadoForm()

        return context



class LivroCreate(generic.CreateView):
    model = Livro
    template_name = 'livros/new.html'
    success_url = reverse_lazy('livros:livros_index')
    #__import__('ipdb').set_trace()
    form_class = LivroForm

class AutorCreate(generic.CreateView):
    model = Autor
    template_name = 'livros/newautor.html'
    success_url = reverse_lazy('livros:livros_new')
    form_class = AutorForm


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


def altera_status_livro(request, livro, user):

    #perfil = get_object_or_404(Perfil, pk=kwargs['user'])
    #estantes = perfil.estante.estantelivro_set.all().order_by('status')
    estante = Estante.objects.get(perfil_dono = request.user.perfil)
    livros_da_estante = estante.livros.all()
    livro = Livro.objects.get(pk=livro)
    #__import__('ipdb').set_trace()
    if (livro in livros_da_estante):
        livro_para_alterar = estante.estantelivro_set.get(livro_adicionado=livro)
        if (livro_para_alterar.status == 'E'):
            livro_para_alterar.status = 'D'
            livro_para_alterar.save()
        elif (livro_para_alterar.status == 'D'):
            livro_para_alterar.status = 'E'
            livro_para_alterar.save()

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


class AvaliaLidoCreate(generic.CreateView):
    model = AvaliaLido
    template_name = 'livros/detail_logado.html'
    success_url = reverse_lazy('livros_index')
    form_class = AvaliaForm

    def form_valid(self, form):
        livro = Livro.objects.get(pk=self.kwargs['pk'])
        form.instance.perfil_avaliador = self.request.user.perfil
        form.instance.livro = livro
        form.instance.lido = True
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['livro'] = get_object_or_404(Livro, pk=self.kwargs['pk'])

        return context


"""
apagar isso se funcionar
def retorna_estantes_com_o_livro(request):
    estantes = Estante.objects.all()
    livro = Livro.objects.get(pk=livro)
    estantes_com_livro = EstanteLivro.objects.filter(livro_adicionado=livro)
"""

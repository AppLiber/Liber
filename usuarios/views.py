#from django.contrib.auth import authenticate, login
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import render


from livros.models import Livro, Categoria
from .forms import CadastroForm


from .models import Perfil, Estante, Emprestimo, AvaliaLido
class UserCreate(generic.CreateView):
    template_name = 'perfil/new.html'
    form_class = CadastroForm
    success_url = reverse_lazy('livros:livros_index')

    def form_valid(self, form):
        user = form.save()
        user.perfil = Perfil.objects.create(telefone=form.cleaned_data['telefone'],
                data_de_nascimento=form.cleaned_data['data_de_nascimento'],
                sexo=form.cleaned_data['sexo'],usuario=user)
                #imagem_perfil=form.cleaned_data['imagem_perfil'])

        user.save()
        user.perfil.estante = Estante.objects.create(perfil_dono = user.perfil)
        user.save()

        return redirect(reverse_lazy('livros_index'))
"""
return redirect(reverse_lazy('usuarios:estante',kwargs={'user':self.kwargs['user']}))

def get_success_url(self):
return reverse_lazy('livros:livros_detail', kwargs={'pk':self.kwargs['pk']})

"""

class UserIndex(generic.ListView):
    template_name = 'usuarios/index.html'
    context_object_name = 'usuario_list'

    def get_queryset(self):
        return Perfil.objects.all()

class UserDetail(generic.DetailView):
    model = Perfil
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        #context['perfil'] = get_object_or_404(Perfil, pk=self.kwargs['user'])
        perfil = self.request.user.perfil
        context['estante_livros'] = perfil.estante.estantelivro_set.all()
        livros_lidos_total = perfil.avalialido_set.all()
        context['livros_lidos_total'] = perfil.avalialido_set.all()
        context['var'] = paginas_lidas_total(self.request)
        context['sugestao'] = sugestoes_por_media_dos_livros(self.request)

        return context

def logout_view(request):
    logout(request)
    return redirect('login')


class PerfilEstanteList(generic.DetailView):
    model = Estante
    template_name = 'dashboard/estante.html'

    def get_object(self):
    #    __import__('ipdb').set_trace()
        usuario = get_object_or_404(Perfil, pk=self.kwargs['user'])
        return Estante.objects.get(perfil_dono=usuario)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['perfil'] = get_object_or_404(Perfil, pk=self.kwargs['user'])
        perfil = get_object_or_404(Perfil, pk=self.kwargs['user'])
        context['estante_livros'] = perfil.estante.estantelivro_set.all()
        return context

        #return get_object_or_404(Estante, usuario_dono_id = self.kwargs['user'])

@login_required
def fazer_pedido_de_emprestimo(request, user, livro):
    perfil_solicitante = request.user.perfil
    perfil_do_dono = get_object_or_404(Perfil, usuario=user)
    livro = Livro.objects.get(pk=livro)

    estante_livro = perfil_do_dono.estante.estantelivro_set.get(livro_adicionado=livro)
    emprestimo = Emprestimo.objects.create(perfil_do_dono=perfil_do_dono, perfil_solicitante=perfil_solicitante, livro_emprestado=estante_livro)

    return redirect('usuarios:estante', user=request.user.perfil.id)

@login_required
def marcar_livro_lido(request, pk):
    perfil = request.user.perfil
    livro = Livro.objects.get(pk=pk)
    livros_lidos = perfil.avalialido_set.all()
    p = perfil.avalialido_set.filter(livro=livro)

    if (livro != p):
        perfil.avalialido_set.create(perfil_avaliador=perfil, livro=livro, lido=True)

    return redirect('livros_index')


def paginas_lidas_total(request):
    perfil = request.user.perfil
    livros_lidos = perfil.avalialido_set.all()
    quantidade_livros_lidos = livros_lidos.count()

    var = 0

    for livro_lido in livros_lidos:
        var += livro_lido.livro.paginas

    return var

def avaliacao_de_livros_por_categoria(request):

    perfil = request.user.perfil
    categorias_preferidas = perfil.categorias_preferidas.all()
    livros_lidos = perfil.avalialido_set.all()
    categorias = Categoria.objects.all()


    lista = {}

    for categoria in categorias:
        nota = 0
        media = 0
        peso = 0
        if categoria in categorias_preferidas:
            peso = 50
        cats = livros_lidos.filter(livro__categorias__descricao=categoria.descricao)
        if cats:
            for cat in cats:
                nota += cat.nota
            media = nota/len(cats) + peso
            lista[categoria.descricao] = media

    return lista

import operator
from livros.views import media_cada_livro

def sugestoes_por_media_dos_livros(request):
    lista = avaliacao_de_livros_por_categoria(request)
    sorted_lista = sorted(lista.items(), key=operator.itemgetter(1))
    sorted_lista.reverse()

    livros = Livro.objects.all()
    lista_livros_sugestao = []

    for item in sorted_lista:
        livros_cat = livros.filter(categorias__descricao=item[0])
        sorted_cat = sorted(livros_cat, key=lambda livro: livro.nota_media())
        sorted_cat.reverse()
        lista_livros_sugestao.extend(sorted_cat)

    return lista_livros_sugestao


class LivrosAvaliados(generic.ListView):
    model = AvaliaLido
    template_name = 'dashboard/avaliacao_livro.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['perfil'] = get_object_or_404(Perfil, pk=self.kwargs['user'])
        perfil = get_object_or_404(Perfil, pk=self.kwargs['user'])
        context['estante_livros'] = perfil.estante.estantelivro_set.all()
        return context

    def get_object(self):
    #    __import__('ipdb').set_trace()
        usuario = get_object_or_404(Perfil, pk=self.kwargs['user'])
        return AvaliaLido.objects.get(perfil_avaliador=usuario)


    def Livros_Avaliados(request, pk):
        perfil = request.user.perfil
        livro = Livro.objects.get(pk=pk)
        #livro_lido = perfil.avalialido_set.get(livro=livro).livro
        livros_lidos = perfil.avalialido_set.all()
    #    l = perfil.avalialido_set.get(livro=pk).livro
        p = perfil.avalialido_set.filter(livro=livro)
        #for livro_lido in livros_lidos:

        #if(livro != livro_lido):
        if (livro != p):
            perfil.avalialido_set.create(perfil_avaliador=perfil, livro=livro, lido=True)

        return livros_lidos


class SugestaoLivro(generic.ListView):

    context_object_name = 'lista_sugere3'
    template_name = 'dashboard/sugestao.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['perfil'] = get_object_or_404(Perfil, pk=self.kwargs['user'])
        perfil = get_object_or_404(Perfil, pk=self.kwargs['user'])
        context['sugestao'] = sugestoes(self.request)
        #__import__('ipdb').set_trace()
        context['teste'] = avaliacao_de_livros_por_categoria(self.request)
        context['teste1'] = sugestoes_por_media_dos_livros(self.request)

        return context

    def get_object(self):
    #    __import__('ipdb').set_trace()
        usuario = get_object_or_404(Perfil, pk=self.kwargs['user'])
        return AvaliaLido.objects.get(perfil_avaliador=usuario)

    def get_queryset(self):
        usuario = get_object_or_404(Perfil, pk=self.kwargs['user'])
        return AvaliaLido.objects.filter(perfil_avaliador=usuario)

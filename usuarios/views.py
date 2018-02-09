#from django.contrib.auth import authenticate, login
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from livros.models import Livro
from .models import Perfil, Estante, Emprestimo, AvaliaLido
from .forms import CadastroForm


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
    #    user.perfil.avalialido_set = AvaliaLido.objects.create(perfil_avaliador = user.perfil)
    #    user.save()

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


        """
        #livros_lidos = perfil.avalialido_set.all()
        quantidade_livros_lidos = livros_lidos_total.count()

        #livro1 = perfil.avalialido_set.first()
        #livro1.livro.paginas
        var = 0
        for livro_lido in livros_lidos_total:
            var += livro_lido.livro.paginas
            return var;

        var
        """

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
    #livro_lido = perfil.avalialido_set.get(livro=livro).livro
    livros_lidos = perfil.avalialido_set.all()
#    l = perfil.avalialido_set.get(livro=pk).livro
    p = perfil.avalialido_set.filter(livro=livro)
    #for livro_lido in livros_lidos:

    #if(livro != livro_lido):
    if (livro != p):
        perfil.avalialido_set.create(perfil_avaliador=perfil, livro=livro, lido=True)

    return redirect('livros_index')


def paginas_lidas_total(request):
    perfil = request.user.perfil
    #livro = Livro.objects.get(pk=livro)
    livros_lidos = perfil.avalialido_set.all()
    quantidade_livros_lidos = livros_lidos.count()

    #livro1 = perfil.avalialido_set.first()
    #livro1.livro.paginas
    var = 0

    for livro_lido in livros_lidos:
        var += livro_lido.livro.paginas

    return var

def media_livro(request):
    livroComNotas = Livro.objects.get(pk=self.kwargs['pk'])
    notas=livroComNotas.avalialido_set.all()
    somaNotas=0
    for nota in notas:
        somaNotas += nota.AvaliaLido.nota
        media=somaNotas/notas.count()
    return media
# def adiciona_livro_na_estante(request):
#     model = Estante
#     template_name = 'dashboard/estante.html'
#     success_url = reverse_lazy('usuarios:estante')
#
#
#
#     Estante.livros.all()

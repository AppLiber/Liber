#from django.contrib.auth import authenticate, login
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from livros.models import Livro
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
    template_name = 'dashboard/index.html', 'dashboard/base_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        #context['perfil'] = get_object_or_404(Perfil, pk=self.kwargs['user'])
        perfil = self.request.user.perfil
        context['estante_livros'] = perfil.estante.estantelivro_set.all()
        livros_lidos_total = perfil.avalialido_set.all()
        context['livros_lidos_total'] = perfil.avalialido_set.all()
        context['var'] = paginas_lidas_total(self.request)
        context['sugestao'] = perfil_de_sugestao(self.request)



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

def perfil_de_sugestao(request):
    perfil = request.user.perfil


    preferidas = perfil.categorias_preferidas.all()

    if preferidas.filter(descricao__icontains='espo'):
        esportepref=50
    if preferidas.filter(descricao__icontains='roma'):
        romancepref=50
    if preferidas.filter(descricao__icontains='dra'):
        dramapref=50
    if preferidas.filter(descricao__icontains='hum'):
        humorepref=50
    if preferidas.filter(descricao__icontains='ajud'):
        autoajudapref=50
    if preferidas.filter(descricao__icontains='reli'):
        religiosoepref=50
    if preferidas.filter(descricao__icontains='cul'):
        culinariapref=50
    if preferidas.filter(descricao__icontains='bib'):
        bibliografiapref=50
    if preferidas.filter(descricao__icontains='fic'):
        ficcaopref=50
    if preferidas.filter(descricao__icontains='fant'):
        fantasiapref=50
    if preferidas.filter(descricao__icontains='ter'):
        terrorpref=50


    esporte=AvaliaLido.objects.filter(perfil_avaliador=perfil).filter(livro__categorias__descricao__icontains='espo')
    romance=AvaliaLido.objects.filter(perfil_avaliador=perfil).filter(livro__categorias__descricao__icontains='roma')
    drama=AvaliaLido.objects.filter(perfil_avaliador=perfil).filter(livro__categorias__descricao__icontains='dra')
    humor=AvaliaLido.objects.filter(perfil_avaliador=perfil).filter(livro__categorias__descricao__icontains='hum')
    autoajuda=AvaliaLido.objects.filter(perfil_avaliador=perfil).filter(livro__categorias__descricao__icontains='ajud')
    religioso=AvaliaLido.objects.filter(perfil_avaliador=perfil).filter(livro__categorias__descricao__icontains='reli')
    culinaria=AvaliaLido.objects.filter(perfil_avaliador=perfil).filter(livro__categorias__descricao__icontains='cul')
    bibliografia=AvaliaLido.objects.filter(perfil_avaliador=perfil).filter(livro__categorias__descricao__icontains='bib')
    ficcao=AvaliaLido.objects.filter(perfil_avaliador=perfil).filter(livro__categorias__descricao__icontains='fic')
    fantasia=AvaliaLido.objects.filter(perfil_avaliador=perfil).filter(livro__categorias__descricao__icontains='fant')
    terror=AvaliaLido.objects.filter(perfil_avaliador=perfil).filter(livro__categorias__descricao__icontains='ter')


#média das avaliações de cada categoria avaliada
    somaNota=0
    for nota in esporte:
        somaNota=0
        media=0
        somaNota= nota.nota
        media=somaNota/esporte.count()
        esporte_nota=media*5
    return esporte_nota

    for nota in romance:
        somaNota=0
        media=0
        somaNota= nota.nota
        media=somaNota/romance.count()
        romance_nota=media*5
    return romance_nota

    for nota in drama :
        somaNota=0
        media=0
        somaNota= nota.nota
        media=somaNota/drama.count()
        drama_nota=media*5
    return drama_nota

    for nota in humor:
        somaNota=0
        media=0
        somaNota= nota.nota
        media=somaNota/humor.count()
        humor_nota=media*5
    return humor_nota

    for nota in autoajuda:
        somaNota=0
        media=0
        somaNota= nota.nota
        media=somaNota/autoajuda.count()
        autoajuda_nota=media*5
    return autoajuda_nota

    for nota in religioso:
        somaNota=0
        media=0
        somaNota= nota.nota
        media=somaNota/religioso.count()
        religioso_nota=media*5
    return religioso_nota

    for nota in culinaria:
        somaNota=0
        media=0
        somaNota= nota.nota
        media=somaNota/culinaria.count()
        culinaria_nota=media*5
    return culinaria_nota

    for nota in bibliografia:
        somaNota=0
        media=0
        somaNota= nota.nota
        media=somaNota/bibliografia.count()
        bibliografia_nota=media*5
    return bibliografia_nota

    for nota in ficcao:
        somaNota=0
        media=0
        somaNota= nota.nota
        media=somaNota/ficcao.count()
        ficcao_nota=media*5
    return ficcao_nota

    for nota in fantasia:
        somaNota=0
        media=0
        somaNota= nota.nota
        media=somaNota/fantasia.count()
        fantasia_nota=media*5
    return fantasia_nota

    for nota in terror:
        somaNota=0
        media=0
        somaNota= nota.nota
        media=somaNota/terror.count()
        terror_nota=media*5
    return terror_nota

# Calculando o total de cada categoria..  preferidas+avaliadas
    esporteTotal=0
    romaceTotal=0
    dramaTotal=0
    humorTotal=0
    autoajudaTotal=0
    religiosoTotal=0
    culinariaTotal=0
    bibliografiaTotal=0
    ficcaoTotal=0
    fantasiaTotal=0
    terrorTotal=0

    esporteTotal=esportepref+esporte_nota
    romaceTotal=romancepref+romance_nota
    dramaTotal=dramapref+drama_nota
    humorTotal=humorepref+humor_nota
    autoajudaTotal=autoajudapref+autoajuda_nota
    religiosoTotal=religiosoepref+religioso_nota
    culinariaTotal=culinariapref+culinaria_nota
    bibliografiaTotal=bibliografiapref+bibliografia_nota
    ficcaoTotal=ficcaopref+ficcao_nota
    fantasiaTotal=fantasiapref+fantasia_nota
    terrorTotal=terrorpref+terror_nota

    listaSugestao=[esporteTotal, romaceTotal, dramaTotal, humorTotal,autoajudaTotal, religiosoTotal, culinariaTotal, bibliografiaTotal, ficcaoTotal, fantasiaTotal, terrorTotal]
    listaSugestao.sort()  #ordenando do menor pro maior
    listaSugestao.reverse()   #invertendo a lista . Agora está do maior pro menor

    for x in range(11): #organizando a lista
        if esporte_nota == listaSugestao[x]:
            lista[x]='esporte'
        if romance_nota == listaSugestao[x]:
            lista[x]='romance'
        if drama_nota == listaSugestao[x]:
            lista[x]='drama'
        if humor_nota == listaSugestao[x]:
            lista[x]='humor'
        if autoajuda_nota == listaSugestao[x]:
            lista[x]='autoajuda'
        if religioso_nota == listaSugestao[x]:
            lista[x]='religioso'
        if culinaria_nota == listaSugestao[x]:
            lista[x]='culinaria'
        if bibliografia_nota == listaSugestao[x]:
            lista[x]='bibliografia'
        if ficcao_nota == listaSugestao[x]:
            lista[x]='ficcao'
        if fantasia_nota == listaSugestao[x]:
            lista[x]='fantasia'
        if terror_nota == listaSugestao[x]:
            lista[x]='terror'

    return listaSugestao  #Aqui já é as categorias ordenadas da maior nota para a menor

    livrossugerido1=Livro.objects.filter(categorias__descricao__icontains=listaSugestao[0])#está retornando uma queryset
    livrossugerido2=Livro.objects.filter(categorias__descricao__icontains=listaSugestao[1])#tente pegar os livros e mostrar no template
    livrossugerido3=Livro.objects.filter(categorias__descricao__icontains=listaSugestao[2])
    livrossugerido4=Livro.objects.filter(categorias__descricao__icontains=listaSugestao[3])
    livrossugerido5=Livro.objects.filter(categorias__descricao__icontains=listaSugestao[4])



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


# def adiciona_livro_na_estante(request):
#     model = Estante
#     template_name = 'dashboard/estante.html'
#     success_url = reverse_lazy('usuarios:estante')
#
#
#
#     Estante.livros.all()

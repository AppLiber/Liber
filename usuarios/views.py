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


from livros.models import Livro
from .forms import CadastroForm, AvaliaForm


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
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        #context['perfil'] = get_object_or_404(Perfil, pk=self.kwargs['user'])
        perfil = self.request.user.perfil
        context['estante_livros'] = perfil.estante.estantelivro_set.all()
        livros_lidos_total = perfil.avalialido_set.all()
        context['livros_lidos_total'] = perfil.avalialido_set.all()
        context['var'] = paginas_lidas_total(self.request)
        context['sugestao'] = sugestoes(self.request)
#        context['sugestao'] = perfil_de_sugestao(self.request)



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
    perfil_do_dono = get_object_or_404(Perfil, pk=user)
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


def sugestoes(request):
    perfil = request.user.perfil

    preferidas = perfil.categorias_preferidas.all()
    a=1
    if a > 0:

        if preferidas.filter(descricao__icontains='espor'):
            esportepref=50
        else:
            esportepref=0
        if preferidas.filter(descricao__icontains='roma'):
            romancepref=50
        else:
            romancepref=0
        if preferidas.filter(descricao__icontains='dra'):
            dramapref=50
        else:
            dramapref=0
        if preferidas.filter(descricao__icontains='hum'):
            humorepref=50
        else:
            humorepref=0
        if preferidas.filter(descricao__icontains='ajud'):
            autoajudapref=50
        else:
            autoajudapref=0
        if preferidas.filter(descricao__icontains='reli'):
            religiosoepref=50
        else:
            religiosoepref=0
        if preferidas.filter(descricao__icontains='cul'):
            culinariapref=50
        else:
            culinariapref=0
        if preferidas.filter(descricao__icontains='bib'):
            bibliografiapref=50
        else:
            bibliografiapref=0
        if preferidas.filter(descricao__icontains='fic'):
            ficcaopref=50
        else:
            ficcaopref=0
        if preferidas.filter(descricao__icontains='fant'):
            fantasiapref=50
        else:
            fantasiapref=0
        if preferidas.filter(descricao__icontains='ter'):
            terrorpref=50
        else:
            terrorpref=0

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

        esporte_nota=0
        romance_nota=0
        drama_nota=0
        humor_nota=0
        autoajuda_nota=0
        religioso_nota=0
        culinaria_nota=0
        bibliografia_nota=0
        ficcao_nota=0
        fantasia_nota=0
        terror_nota=0


    #média das avaliações de cada categoria avaliada

        somaNota=0

        for nota in esporte:
            somaNota+= nota.nota
            media=somaNota/esporte.count()
            qtd= 5*esporte.count()
            esporte_nota=media*5+qtd

        for nota in romance:
            somaNota=0
            media=0
            somaNota= nota.nota
            media=somaNota/romance.count()
            qtd= 5*romance.count()
            romance_nota=media*5

        for nota in drama :
            somaNota=0
            media=0
            somaNota+= nota.nota
            media=somaNota/drama.count()
            qtd= 5*drama.count()
            drama_nota=media*5+qtd

        for nota in humor:
            somaNota=0
            media=0
            somaNota+= nota.nota
            media=somaNota/humor.count()
            qtd= 5*humor.count()
            humor_nota=media*5+qtd

        for nota in autoajuda:
            somaNota=0
            media=0
            somaNota+= nota.nota
            media=somaNota/autoajuda.count()
            qtd= 5*autoajuda.count()
            autoajuda_nota=media*5+qtd

        for nota in religioso:
            somaNota=0
            media=0
            somaNota+= nota.nota
            media=somaNota/religioso.count()
            qtd= 5*religioso.count()
            religioso_nota=media*5+qtd

        for nota in culinaria:
            somaNota=0
            media=0
            somaNota+= nota.nota
            media=somaNota/culinaria.count()
            qtd= 5*culinaria.count()
            culinaria_nota=media*5+qtd


        for nota in bibliografia:
            somaNota=0
            media=0
            somaNota+= nota.nota
            media=somaNota/bibliografia.count()
            qtd= 5*bibliografia.count()
            bibliografia_nota=media*5+qtd

        for nota in ficcao:
            somaNota=0
            media=0
            somaNota+= nota.nota
            media=somaNota/ficcao.count()
            qtd= 5*ficcao.count()
            ficcao_nota=media*5+qtd

        for nota in fantasia:
            somaNota=0
            media=0
            somaNota+= nota.nota
            media=somaNota/fantasia.count()
            qtd= 5*fantasia.count()
            fantasia_nota=media*5+qtd

        for nota in terror:
            somaNota=0
            media=0
            somaNota+= nota.nota
            media=somaNota/terror.count()
            qtd= 5*terror.count()
            terror_nota=media*5+qtd

    # Calculando o total de cada categoria..  preferidas+avaliadas
        esporteTotal=0
        romanceTotal=0
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
        romanceTotal=romancepref+romance_nota
        dramaTotal=dramapref+drama_nota
        humorTotal=humorepref+humor_nota
        autoajudaTotal=autoajudapref+autoajuda_nota
        religiosoTotal=religiosoepref+religioso_nota
        culinariaTotal=culinariapref+culinaria_nota
        bibliografiaTotal=bibliografiapref+bibliografia_nota
        ficcaoTotal=ficcaopref+ficcao_nota
        fantasiaTotal=fantasiapref+fantasia_nota
        terrorTotal=terrorpref+terror_nota

        listaSugestao=[esporteTotal, romanceTotal, dramaTotal, humorTotal,autoajudaTotal, religiosoTotal, culinariaTotal, bibliografiaTotal, ficcaoTotal, fantasiaTotal, terrorTotal]
        listaSugestao.sort()  #ordenando do menor pro maior
        listaSugestao.reverse()   #invertendo a lista . Agora está do maior pro menor



        for x in range(11): #organizando a lista
            if esporteTotal == listaSugestao[x]:
                listaSugestao[x]='esporte'
            if romanceTotal == listaSugestao[x]:
                listaSugestao[x]='romance'
            if dramaTotal == listaSugestao[x]:
                listaSugestao[x]='drama'
            if humorTotal == listaSugestao[x]:
                listaSugestao[x]='humor'
            if autoajudaTotal== listaSugestao[x]:
                listaSugestao[x]='autoajuda'
            if religiosoTotal == listaSugestao[x]:
                listaSugestao[x]='religioso'
            if culinariaTotal == listaSugestao[x]:
                listaSugestao[x]='culinaria'
            if bibliografiaTotal == listaSugestao[x]:
                listaSugestao[x]='bibliografia'
            if ficcaoTotal == listaSugestao[x]:
                listaSugestao[x]='ficcao'
            if fantasiaTotal == listaSugestao[x]:
                listaSugestao[x]='fantasia'
            if terrorTotal == listaSugestao[x]:
                listaSugestao[x]='terror'


        livrossugerido1=AvaliaLido.objects.filter(livro__categorias__descricao__icontains=listaSugestao[0])#está retornando uma queryset
        livrossugerido2=AvaliaLido.objects.filter(livro__categorias__descricao__icontains=listaSugestao[1])#tente pegar os livros e mostrar no template
        livrossugerido3=AvaliaLido.objects.filter(livro__categorias__descricao__icontains=listaSugestao[2])
        livrossugerido4=AvaliaLido.objects.filter(livro__categorias__descricao__icontains=listaSugestao[3])
        livrossugerido5=AvaliaLido.objects.filter(livro__categorias__descricao__icontains=listaSugestao[4])

        lista_todos =[livrossugerido1.order_by('-nota'), livrossugerido2.order_by('-nota'), livrossugerido3.order_by('-nota'), livrossugerido4.order_by('-nota'), livrossugerido5.order_by('-nota')]

        lista_final = []

        for sugere in lista_todos:
                for sug in sugere:
                    if sug not in lista_final:
                        lista_final.append(sug)

        livrosLidos=perfil.avalialido_set.all()

        listafinalfinal=[]
        for y in livrosLidos:
            for x in lista_final:
                if x.livro.titulo == y.livro.titulo:
                    lista_final.remove(x)

        return lista_final




        return render(request, 'sugestao.html', {"lista_sugere3": lista})


class LivrosAvaliados(generic.ListView):
    model = AvaliaLido
    #template_name = 'dashboard/avaliacao_livro.html'

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

class SugestaoLivro(generic.ListView):

    context_object_name = 'lista_sugere3'
    template_name = 'dashboard/sugestao.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['perfil'] = get_object_or_404(Perfil, pk=self.kwargs['user'])
        perfil = get_object_or_404(Perfil, pk=self.kwargs['user'])
        context['sugestao'] = sugestoes(self.request)
        #__import__('ipdb').set_trace()

        return context

    def get_object(self):
    #    __import__('ipdb').set_trace()
        usuario = get_object_or_404(Perfil, pk=self.kwargs['user'])
        return AvaliaLido.objects.get(perfil_avaliador=usuario)

    def get_queryset(self):
        usuario = get_object_or_404(Perfil, pk=self.kwargs['user'])
        return AvaliaLido.objects.filter(perfil_avaliador=usuario)
"""
def livro3(request):
    perfil=request.user.perfil
    sugestao=sugestoes(request)
    lista3=[]
    for i in range(len(sugestao)):
        lista3.append(sugestao[i].titulo)
    return lista3
"""

class AvaliaLidoCreate(generic.CreateView):
    model = AvaliaLido
    template_name = 'dashboard/avaliacao.html'
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


class Avaliacao (generic.ListView):

    context_object_name = 'lista_sugere3'
    template_name = 'dashboard/avaliacao_livro.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['perfil'] = get_object_or_404(Perfil, pk=self.kwargs['user'])
        perfil = get_object_or_404(Perfil, pk=self.kwargs['user'])
        context['sugestao'] = sugestoes(self.request)
        #__import__('ipdb').set_trace()

        return context

    def get_object(self):
    #    __import__('ipdb').set_trace()
        usuario = get_object_or_404(Perfil, pk=self.kwargs['user'])
        return AvaliaLido.objects.get(perfil_avaliador=usuario)

    def get_queryset(self):
        usuario = get_object_or_404(Perfil, pk=self.kwargs['user'])
        return AvaliaLido.objects.filter(perfil_avaliador=usuario)



class historico_emprestimo (generic.ListView):

    context_object_name = 'emprestimos'
    template_name = 'dashboard/emprestimos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['perfil'] = get_object_or_404(Perfil, pk=self.kwargs['user'])
        perfil = get_object_or_404(Perfil, pk=self.kwargs['user'])
        context['sugestao'] = sugestoes(self.request)
        #__import__('ipdb').set_trace()

        return context

    def get_object(self):
    #    __import__('ipdb').set_trace()
        usuario = get_object_or_404(Perfil, pk=self.kwargs['user'])
        return AvaliaLido.objects.get(perfil_avaliador=usuario)

    def get_queryset(self):
        usuario = get_object_or_404(Perfil, pk=self.kwargs['user'])
        return AvaliaLido.objects.filter(perfil_avaliador=usuario)

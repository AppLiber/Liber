#from django.contrib.auth import authenticate, login
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import logout
# from django.contrib.auth.decorators import login_required

from livros.models import Livro
from .models import Perfil
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

        return redirect(reverse_lazy('livros:livros_index'))


class UserIndex(generic.ListView):
    template_name = 'usuarios/index.html'
    context_object_name = 'usuario_list'

    def get_queryset(self):
        return Perfil.objects.all()


def logout_view(request):
    logout(request)
    return redirect('login')

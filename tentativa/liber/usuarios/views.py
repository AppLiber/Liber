from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from .models import Usuario
from .forms import UsuarioForm

class UsuarioIndex(generic.ListView):
    template_name = 'usuarios/index.html'
    context_object_name = 'usuario_list'

    def get_queryset(self):
        return Usuario.objects.all()

class UsuarioDetail(generic.DetailView):
    model = Usuario
    template_name = 'usuarios/detail.html'

class UsuarioCreate(generic.CreateView):
    model = Usuario
    template_name = 'usuarios/new.html'
    success_url = reverse_lazy('usuarios:usuarios_index')
    form_class = UsuarioForm

class UsuarioUpdate(generic.UpdateView):
    model = Usuario
    template_name = 'usuarios/edit.html'
    form_class = UsuarioForm

    def get_success_url(self):
        return reverse_lazy('usuarios:usuarios_detail', kwargs={'pk':self.kwargs['pk']})

class UsuarioDelete(generic.DeleteView):
    model = Usuario
    success_url = reverse_lazy('usuarios:usuarios_index')

from django.shortcuts import render, redirect, get_object_or_404

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.forms import ModelForm


from .models import *

#class IndexView(generic.ListView):
#    template_name='usuarios.html'
#    context_object_name

class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome']

def cadastrar_usuario(request, template_name='usuario_form.html'):
    form = UsuarioForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect ('listar_usuario')
    return render(request, template_name, {'form': form})

def listar_usuario(request, template_name="usuarios_list.html"):
    usuario = Usuario.objects.all()
    usuarios = {'lista': usuario}
    return render(request, template_name, usuarios)

def editar_usuario(request, pk, template_name='usuario_form.html'):
    usuario = get_object_or_404(Usuario, pk = pk)
    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('usuarios:listar_usuario')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, template_name, {'form': form})

def remover_usuario (request, pk, template_name='usuario_delete.html'):
    usuario = Usuario.objects.get(pk=pk)
    if request.method == "POST":
        usuario.delete()
        return redirect('usuarios:listar_usuario')
    return render(request, template_name, {'usuario':usuario})

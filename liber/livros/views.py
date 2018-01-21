from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import *

class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'lista_livros'

    def get_queryset(self):
        return Livro.objects.order_by('titulo')

class DetailView(generic.DetailView):
    model = Livro
    template_name = 'detalhar_livro.html'

#def IndexView(request):
    #lista_livros = Livro.objects.order_by('titulo')
    #context= {'lista_livros': lista_livros}
    #return render(request, 'index.html', context)

#def detalhar_livro(request, livro_id):
#    try:
#        livro = Livro.objects.get(pk=livro_id)
#    except Livro.DoesNotExist:
#        raise Http404("Nao existe")
#    return render(request, 'detalhar_livro.html', {'livro':livro})

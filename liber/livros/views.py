from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import *

from .models import *

class LivroIndex(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'lista_livros'

    def get_queryset(self):
        return Livro.objects.order_by('titulo')

class LivroCreate(generic.CreateView):
    model = Livro
    template_name = 'livros/new.html'
    success_url = reverse_lazy('livros_index')
    form_class = LivroForm

class LivroDetail(generic.DetailView):
    model = Livro
    template_name = 'livros/detail.html'

    #Livros.objects.get(pk=self.kwargs['pk'])

class LivroDelete(generic.DeleteView):
    model = Livro
    sucess_url = reverse_lazy('livros:index')

    #def get_success_url(self):
    #    return reverse_lazy('livros_detalhe', kwargs={'pk':self.kwargs['pk']})


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

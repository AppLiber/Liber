from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def detalhar_livro(request, livro_id):
    pass

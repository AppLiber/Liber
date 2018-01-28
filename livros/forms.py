from django.forms import ModelForm

from .models import Autor, Categoria, Livro

class LivroForm(ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'editora', 'descricao', 'nota', 'autores', 'imagem']

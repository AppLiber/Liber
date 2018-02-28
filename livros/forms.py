from django.forms import ModelForm

from .models import Autor, Categoria, Livro

class LivroForm(ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'editora', 'isbn10', 'isbn13', 'descricao', 'paginas', 'autores', 'edicao', 'ano', 'categorias', 'imagem']


class AutorForm(ModelForm):
    class Meta:
        model = Autor
        fields = ['nome', 'sobrenome']

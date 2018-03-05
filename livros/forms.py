from django.forms import ModelForm
from django import forms

from .models import Autor, Categoria, Livro

class LivroForm(ModelForm):
    #autores = forms.ModelMultipleChoiceField(queryset=Autor.objects.all(), required=False, widget=forms.CheckboxSelectMultiple())
    #categorias = forms.ModelMultipleChoiceField(queryset=Categoria.objects.all(), required=False, widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Livro
        fields = ['titulo', 'editora', 'isbn10', 'isbn13', 'descricao', 'paginas', 'autores', 'edicao', 'ano', 'categorias' ] #, 'imagem']


class AutorForm(ModelForm):
    class Meta:
        model = Autor
        fields = ['nome', 'sobrenome']

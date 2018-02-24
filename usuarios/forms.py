from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Perfil, AvaliaLido, Emprestimo

class CadastroForm(UserCreationForm):

    telefone = forms.CharField()
    data_de_nascimento = forms.DateField()
    sexo = forms.CharField()
    #imagem_perfil = forms.ImageField()

    class Meta:
        model = User
        fields = ('username','password1','password2','telefone','data_de_nascimento','sexo')

"""
class RegistrarUsuarioForm(forms.Form):

    nome = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    senha = forms.CharField(required=True)
    telefone = forms.CharField(required=True)
    data_de_nascimento = forms.DateField(required=True)
    sexo = forms.CharField(required=True)
    imagem_perfil = forms.ImageField(required=False)

    def is_valid(self):
        valid = True
        if not super(RegistrarUsuarioForm, self).is_valid():
            self.adiciona_erro('Por favor verifique os dados informados.')
            valid = False

        user_exists = User.objects.filter(username=self.data['email']).exists()

        if user_exists:
            self.adiciona_erro('Usuário ja existente')
            valid = False
        return valid

    def adiciona_erro(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
        errors.append(message)
"""

class AvaliaForm(ModelForm):
    class Meta:
        model = AvaliaLido
        fields = ['nota']


class EmprestimoForm(ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['data_devolucao', 'mensagem_cancelamento']

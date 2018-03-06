from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Perfil, AvaliaLido, Emprestimo, AvaliaEmprestimo

SEXO_USUARIO = (
    ('F', 'Feminino'),
    ('M', 'Masculino'),
)

class CadastroForm(UserCreationForm):

    telefone = forms.CharField()
    data_de_nascimento = forms.DateField()
    sexo = forms.ChoiceField(widget=forms.Select, choices=SEXO_USUARIO) #SelectCharWidget(sexo=SEXO_USUARIO))
    #imagem_perfil = forms.ImageField()

    class Meta:
        model = User
        fields = ('username','password1','password2','telefone','data_de_nascimento','sexo')#,'imagem_perfil')

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
        fields = ['nota','comentario']

class PedirLivroEmprestadoForm(ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['data_devolucao', 'mensagem_de_quem_pede']

class EmprestimoForm(ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['mensagem_resposta']
        #mensagem_de_quem_pede = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':1,'cols':10,'placeholder':'keword values'}))


class AvaliacaoEmprestimoForm(ModelForm):
    class Meta:
        model = AvaliaEmprestimo
        fields = ['nota','mensagem_de_avaliacao']

from django.db import models

from livros.models import Livro

from django.contrib.auth.models import User

SEXO_USUARIO = (
    ('F', 'Feminino'),
    ('M', 'Masculino'),
)

class Perfil(models.Model):

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # nome = models.CharField(max_length=255, null=False)
    # email = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=15, null=True)
    data_de_nascimento = models.DateField(blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_USUARIO, blank=True, null=True)
    #imagem_perfil = models.ImageField(upload_to='imagem_perfil/', default='imagem_perfil/user.png')

    #contatos = models.ManyToManyField('self')

"""
    @property
    def email(self):
        return self.usuario.email
"""

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

    def __str__(self):
        return self.usuario.username

    class Meta:
        verbose_name='Perfil'
        verbose_name_plural= "Perfis"


"""
    @property
    def email(self):
        return self.usuario.email
"""


class Estante(models.Model):

    nome = models.CharField(max_length=30, blank=False , default="Estante")
    # perfil_dono
    perfil_dono = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    livros = models.ManyToManyField('livros.Livro') # Livro
    disponível = models.BooleanField()

    def __str__(self):
        return self.nome

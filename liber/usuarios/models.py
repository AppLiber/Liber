#from datetime import date
#
#from django.contrib.auth.base_uer import AbstractBaseUser
#from django.contrib.auth.models import PermissionMixin
from django.db import models

from livros.models import *
#from .usermanager import UserManager

class Estante(models.Model):
    livros = models.ManyToManyField(Livro)
    nome = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.nome

class Usuario(models.Model):

    nome = models.CharField(max_length=255, null=False)
    estante = models.ForeignKey(Estante, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse()
    #email = models.EmailField(unique=True)
    #senha = models.CharField(max_length=10)
    #sexo = models.CharField(max_length=10)
    #sexo = models.CharField(choices=SEX_CHOICE, max_length=10, default=SEX_M)
    #data_de_nascimento = models.DateField(blank=False)

    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = []
    #objects = UserManager()

    #def get_short_name(self):
    #    return self.name


#SEX_M = 'M'
#SEX_F = 'F'

#SEX_CHOICE = (
#    (SEX_M, 'Masculino'),
#    (SEX_F, 'Feminino')
#)

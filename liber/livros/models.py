from django.db import models

class Autor(models.Model):

    nome = models.CharField(max_length=255, null=False)
    sobrenome = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.nome

class Categoria(models.Model):

    descricao = models.CharField(max_length=255)

class Livro(models.Model):

    titulo = models.CharField(max_length=255, null=False)
    editora = models.CharField(max_length=255, null=False)
    descricao = models.CharField(max_length=255, null=False)
    nota = models.CharField(max_length=2)
    autores = models.ManyToManyField(Autor)

    def __str__(self):
        return self.titulo

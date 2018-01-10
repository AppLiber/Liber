from django.db import models

class Livro(models.Model):

    titulo = models.CharField(max_length=255, null=False)
    editora = models.CharField(max_length=255, null=False)
    isbn = models.CharField(max_length=255)
    isbn2 = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=255, null=False)
    nota = models.CharField(max_length=255, null=False)
    paginas = models.CharField(max_length=255, null=False)
    edicao = models.CharField(max_length=255, null=False)

from django.db import models

class Autor(models.Model):

    nome = models.CharField(max_length=100, null=False)
    sobrenome = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.nome

class Categoria(models.Model):

    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao

class Livro(models.Model):

    titulo = models.CharField(max_length=200, null=False)
    editora = models.CharField(max_length=200, null=False)
    descricao = models.TextField()
    nota = models.DecimalField(max_digits=2, decimal_places=1)
    imagem = models.ImageField(upload_to='imagem_livro/', default='imagem_livro/livro.png')
    autores = models.ManyToManyField(Autor)
    categorias = models.ManyToManyField(Categoria)

    def __str__(self):
        return self.titulo

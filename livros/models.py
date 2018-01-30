from django.db import models

class Autor(models.Model):

    nome = models.CharField(max_length=100, null=False)
    sobrenome = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name='Autor'
        verbose_name_plural= "Autores"


class Categoria(models.Model):

    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao

class Livro(models.Model):
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    titulo = models.CharField(max_length=200, null=False)
    editora = models.CharField(max_length=200, null=False)
    descricao = models.TextField()
    paginas = models.IntegerField(null=False)
#    nota = models.DecimalField(max_digits=2, decimal_places=1)
    imagem = models.ImageField(upload_to='imagem_livro/', default='imagem_livro/livro.png')
    autores = models.ManyToManyField(Autor)
    categorias = models.ManyToManyField(Categoria)

    def __str__(self):
        return self.titulo

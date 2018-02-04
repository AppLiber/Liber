from django.db import models

from livros.models import Livro, Categoria

from django.contrib.auth.models import User

SEXO_USUARIO = (
    ('F', 'Feminino'),
    ('M', 'Masculino'),
)

NOTA_LIDO = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
)


class Perfil(models.Model):

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    telefone = models.CharField(max_length=15, null=True)
    data_de_nascimento = models.DateField(blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_USUARIO, blank=True , null=True)
    categorias_preferidas = models.ManyToManyField(Categoria)
    imagem_perfil = models.ImageField(upload_to='imagem_perfil/', default='imagem_perfil/user.png')


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
STATUS_LIVRO = (
    ('D', 'Disponível'),
    ('E', 'Emprestado'),
)

class Estante(models.Model):

    nome = models.CharField(max_length=30, blank=False , default="Estante")
    perfil_dono = models.OneToOneField(Perfil,  on_delete=models.CASCADE, null=True) #ver esse nulo depois ??!!
    livros = models.ManyToManyField(Livro, through='EstanteLivro')

    def __str__(self):
        return '{}-> {}'.format(self.nome, self.perfil_dono)


class EstanteLivro(models.Model): 
    estante = models.ForeignKey(Estante, on_delete=models.CASCADE)
    livro_adicionado = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_adicionado = models.DateField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_LIVRO, blank=False , null=False, default='D')

class AvaliaLido (models.Model):

    lido = models.BooleanField()
    perfil_Avaliador= models.ForeignKey(Perfil, on_delete=models.CASCADE)
    livros = models.ForeignKey(Livro,  on_delete=models.CASCADE) # Livro
    nota = models.IntegerField(choices=NOTA_LIDO) # ver se nao é char

    #def __str__(self):
    #    return self.livros, self.perfil_Avaliador
    def __str__(self):
        return '{} {} {}'.format(self.livros, self.perfil_Avaliador, self.nota)


class Emprestimo (models.Model):
    perfil_do_dono = models.OneToOneField(Perfil, on_delete=models.CASCADE, related_name="solicitado")
    perfil_solicitante = models.OneToOneField(Perfil, on_delete=models.CASCADE, related_name="solicitante") #on_delete=models.CASCADE,
    livro_emprestado = models.OneToOneField(Estante, on_delete=models.CASCADE) # livro da estante
    data_emprestimo= models.DateField(auto_now=True)
    data_devolucao= models.DateField()

    def __str__(self):
        return self.perfil_do_dono


class AvaliaEmprestimo (models.Model):
    nota = models.IntegerField(choices=NOTA_LIDO)
    Emprestimo_avaliado = models.OneToOneField(Emprestimo, on_delete=models.CASCADE)

    def __str__(self):
        return self.Emprestimo_avaliado

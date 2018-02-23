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

STATUS_EMPRESTIMO = (
    ('S', "Solicitado"),
    ('EA', 'Em andamento'),
    ('OK', 'Concluído'),
    ('C', 'Cancelado')
)


class Perfil(models.Model):

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    telefone = models.CharField(max_length=15, null=True)
    data_de_nascimento = models.DateField(blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_USUARIO, blank=True , null=True)
    categorias_preferidas = models.ManyToManyField(Categoria)
    imagem_perfil = models.ImageField(upload_to='imagem_perfil/', default='imagem_perfil/user.png')
    livros = models.ManyToManyField(Livro, through='AvaliaLido' )


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
    perfil_dono = models.OneToOneField(Perfil,  on_delete=models.CASCADE, null=True)
    livros = models.ManyToManyField(Livro, through='EstanteLivro')

    def __str__(self):
        return '{}-> {}'.format(self.nome, self.perfil_dono)


class EstanteLivro(models.Model):
    estante = models.ForeignKey(Estante, on_delete=models.CASCADE)
    livro_adicionado = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_adicionado = models.DateField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_LIVRO, blank=False , null=False, default='D')

    def __str__(self):
        return '{}-> {}'.format(self.estante, self.livro_adicionado)

class AvaliaLido (models.Model):

    lido = models.BooleanField(default=False)
    perfil_avaliador= models.ForeignKey(Perfil, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    nota = models.IntegerField(choices=NOTA_LIDO, null=False)

    def __str__(self):
        return '{} {} {}'.format(self.livro, self.perfil_avaliador, self.nota)


class Emprestimo (models.Model):
    perfil_do_dono = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="solicitado")
    perfil_solicitante = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="solicitante")
    livro_emprestado = models.ForeignKey(EstanteLivro, on_delete=models.CASCADE)
    data_emprestimo= models.DateField(auto_now=True)
    data_devolucao= models.DateField(null=True)
    status_emprestimo = models.CharField(max_length=2, choices=STATUS_EMPRESTIMO, blank=False , null=False, default='S')
    mensagem_cancelamento = models.TextField(null=True, blank=True)

    def __str__(self):
        return'Dono >{}, para {},{}'.format(self.perfil_do_dono.usuario.username, self.perfil_solicitante, self.livro_emprestado)


class AvaliaEmprestimo (models.Model):
    nota = models.IntegerField(choices=NOTA_LIDO)
    Emprestimo_avaliado = models.OneToOneField(Emprestimo, on_delete=models.CASCADE)

    def __str__(self):
        return self.Emprestimo_avaliado

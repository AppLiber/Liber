from django.db import models

from livros.models import Livro

from django.contrib.auth.models import User

SEXO_USUARIO = (
    ('F', 'Feminino'),
    ('M', 'Masculino'),
)

NOTA_LIDO = (
    ('01', '01'),
    ('02', '02'),
    ('03', '03'),
    ('04', '04'),
    ('05', '05'),
    ('06', '06'),
    ('07', '07'),
    ('08', '08'),
    ('09', '09'),
    ('10', '10'),
)
class Perfil(models.Model):

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # nome = models.CharField(max_length=255, null=False)
    # email = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=15, null=True)
    data_de_nascimento = models.DateField(blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_USUARIO, blank=True , null=True)
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

class AvaliaLido (models.Model):
    nota = models.IntegerField(choices=NOTA_LIDO)
    # perfil_dono
    lido = models.BooleanField()
    perfil_dono = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    livros = models.ManyToManyField('livros.Livro') # Livro

    def __str__(self):
        return self.nota


class Emprestimo (models.Model):
    perfil_do_dono = models.OneToOneField(Perfil, on_delete=models.CASCADE, related_name="solicitado")
    perfil_solicitante = models.OneToOneField(Perfil, on_delete=models.CASCADE, related_name="solicitante")
    livro_emprestado = models.OneToOneField(Estante, on_delete=models.CASCADE)
    data_emprestimo= models.DateField(auto_now=True)
    data_devolucao= models.DateField()

    def __str__(self):
        return self.perfil_do_dono


class AvaliaEmpréstimo (models.Model):
    nota = models.IntegerField(choices=NOTA_LIDO)
    Emprestimo_avaliado = models.OneToOneField(Emprestimo, on_delete=models.CASCADE)

    def __str__(self):
        return self.Emprestimo_avaliado

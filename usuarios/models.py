from django.db import models

from livros.models import Livro, Categoria

from django.contrib.auth.models import User

SEXO_USUARIO = (
    ('F', 'Feminino'),
    ('M', 'Masculino'),
)

NOTA_LIDO = (
    ('01', 1),
    ('02', 2),
    ('03', 3),
    ('04', 4),
    ('05', 5),
    ('06', 6),
    ('07', 7),
    ('08', 8),
    ('09', 9),
    ('10', 10),
)


class Perfil(models.Model):

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # nome = models.CharField(max_length=255, null=False)
    # email = models.CharField(max_length=255, null=Falseone
    telefone = models.CharField(max_length=15, null=True)
    data_de_nascimento = models.DateField(blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_USUARIO, blank=True , null=True)
    categorias_preferidas = models.ManyToManyField("livros.Categoria")

#    preferido1 = models.OneToOneField('livros.Categoria' , on_delete=models.CASCADE, related_name="Preferido1" , default = "drama", unique= True, null=True, blank=True)
#    preferido2 = models.OneToOneField('livros.Categoria' , on_delete=models.CASCADE, related_name="Preferido2" , default = "", unique= True) #,, null=True, blank=True)
#    preferido3 = models.OneToOneField('livros.Categoria' , on_delete=models.CASCADE, related_name="Preferido3" , default = "", unique= True) #,, null=True, blank=True)
#    preferido4 = models.OneToOneField('livros.Categoria' , on_delete=models.CASCADE, related_name="Preferido4" , default = "", unique= True, null=True, blank=True)
#    preferido5 = models.OneToOneField('livros.Categoria' , on_delete=models.CASCADE, related_name="Preferido5" , default = "", unique= True, null=True, blank=True)

    imagem_perfil = models.ImageField(upload_to='imagem_perfil/', default='imagem_perfil/user.png')

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
STATUS_LIVRO = (
    ('D', 'Disponível'),
    ('E', 'Emprestado'),
)

class Estante(models.Model):

    nome = models.CharField(max_length=30, blank=False , default="Estante")
    # perfil_dono
    perfil_dono = models.OneToOneField(Perfil, on_delete=models.CASCADE, null=True) #ver esse nulo depois ??!!
    livros = models.ManyToManyField('livros.Livro') # Livro
    #livros_estante = models.ManyToManyField('livros.Livro', through='EstanteLivro')
    status = models.CharField(max_length=1, choices=STATUS_LIVRO, blank=True , null=True)
    #status = models.ForeignKey('self', null=True, related_name)

    def __str__(self):
        return self.nome


"""
class EstanteLivro(models.Model):
    estante = models.ForeignKey(Estante, on_delete=models.CASCADE)
    livro_adicionado = models.ForeignKey(Estante.livros, on_delete=models.CASCADE)
    data_adicionado = models.DateField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_LIVRO, blank=True , null=True)
"""

class AvaliaLido (models.Model):
    # perfil_dono
    lido = models.BooleanField()
    perfil_Avaliador= models.OneToOneField(Perfil, on_delete=models.CASCADE)
    livros = models.ManyToManyField('livros.Livro') # Livro
    nota = models.IntegerField(choices=NOTA_LIDO) # ver se nao é char

    def __str__(self):
        return self.nota


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

from django.db import models


SEXO_USUARIO = (
    ('F', 'Feminino'),
    ('M', 'Masculino'),
)

class Usuario(models.Model):

    nome = models.CharField(max_length=200, blank=False, default="")
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=13, null=False)
    data_de_nascimento = models.DateField(blank=False)
    sexo = models.CharField(max_length=1, choices=SEXO_USUARIO, blank=False, null=False)
    imagem_perfil = models.ImageField(upload_to='imagem_perfil/', default='imagem_perfil/user.png')

    def __str__(self):
        return self.nome

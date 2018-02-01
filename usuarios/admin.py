from django.contrib import admin

from .models import Perfil, Estante, AvaliaLido, Emprestimo, AvaliaEmpréstimo

admin.site.register(Perfil)
admin.site.register(Estante)
admin.site.register(AvaliaLido)
admin.site.register(Emprestimo)
admin.site.register(AvaliaEmpréstimo)

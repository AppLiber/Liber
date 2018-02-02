from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Perfil, Estante, AvaliaLido, Emprestimo, AvaliaEmprestimo

#admin.site.register(Perfil)
admin.site.register(Estante)
admin.site.register(AvaliaLido)
admin.site.register(Emprestimo)
admin.site.register(AvaliaEmprestimo)

class PerfilInLine(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfis'
    fk_name = 'usuario'

class CustomUserAdmin(UserAdmin):
    inlines = (PerfilInLine, )


    def get_inlines_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inlines_instances(request,obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


"""
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = (User,'telefone','data_de_nascimento','sexo')
    list_filter = ('sexo','data_de_nascimento')

    fieldsets = (
        (None, {
            'fields' : (User,'telefone')
        }),
        ('Teste',{
            'fields': ('sexo', 'data_de_nascimento')
        }),
    )
"""

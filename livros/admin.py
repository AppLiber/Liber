from django.contrib import admin

from .models import (Autor, Categoria, Livro)

admin.site.register(Autor)
admin.site.register(Categoria)
admin.site.register(Livro)

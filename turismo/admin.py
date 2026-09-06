from django.contrib import admin
from .models import Categoria, Lugar, PerfilUsuario, Resena

# Configuraciones para que el admin se vea profesional
class LugarAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'latitud', 'longitud')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('categoria',)

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nacionalidad', 'edad')

admin.site.register(Categoria)
admin.site.register(Lugar, LugarAdmin)
admin.site.register(PerfilUsuario, PerfilAdmin)
admin.site.register(Resena)
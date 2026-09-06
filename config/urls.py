from django.contrib import admin
from django.urls import path, include
from django.conf import settings                  # <-- Falta esto
from django.conf.urls.static import static        # <-- Falta esto

urlpatterns = [
    path('admin/', admin.site.urls),
    # Esto envía el tráfico a turismo/urls.py
    path('', include('turismo.urls')), 
]                                                 # <-- El corchete se cierra AQUÍ

# El bloque "if" va AFUERA de la lista, completamente abajo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
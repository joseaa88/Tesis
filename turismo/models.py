from django.db import models
from django.contrib.auth.models import User

# 1. Categorías (Para HU03 - Filtrado)
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=50, default="📍", help_text="Emoji o clase de icono")

    def __str__(self):
        return self.nombre

# 2. Atractivos Turísticos (Para HU02, HU04 - Listado y Detalle)
class Lugar(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    imagen = models.ImageField(upload_to='lugares/', null=True, blank=True)
    
    # Geolocalización (Para el mapa)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    direccion = models.CharField(max_length=255, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="0 para gratis")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Lugar"
        verbose_name_plural = "Lugares"

    def __str__(self):
        return self.nombre

# 3. Perfil de Usuario (Para HU01, HU06 - Intereses)
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # Aquí guardamos qué le gusta al usuario para el Random Forest (HU05)
    intereses = models.ManyToManyField(Categoria, blank=True, related_name="interesados")
    
    # Datos demográficos simples para mejorar la predicción
    edad = models.PositiveIntegerField(null=True, blank=True)
    nacionalidad = models.CharField(max_length=100, default="Peruano")

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

# 4. Reseñas (Para HU08 - Feedback)
class Resena(models.Model):
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name="resenas")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    calificacion = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) # 1 a 5 estrellas
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.lugar.nombre}"
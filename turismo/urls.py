from django.urls import path
from django.contrib.auth import views as auth_views # <--- IMPORTANTE: Vistas de seguridad de Django
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lugar/<int:lugar_id>/', views.detalle_lugar, name='detalle_lugar'),
    path('registro/', views.registro, name='registro'),
    
    # NUEVAS RUTAS: Iniciar y Cerrar Sesión
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]
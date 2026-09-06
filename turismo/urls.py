from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Portada y Catálogo con IA
    path('', views.landing, name='landing'),
    path('explorar/', views.index, name='index'),
    path('lugar/<int:lugar_id>/', views.detalle_lugar, name='detalle_lugar'),
    path('mapa/', views.mapa_turistico, name='mapa'),

    # HU03: Búsqueda dinámica Fetch API (Sprint 3)
    path('api/buscar-lugares/', views.api_buscar_lugares, name='api_buscar_lugares'),

    # HU07: Agenda de Eventos Locales (Sprint 3)
    path('eventos/', views.eventos_publicos, name='eventos_publicos'),
    path('admin/eventos/crear/', views.evento_crear, name='evento_crear'),

    # HU09: Métrica al compartir en redes (Sprint 3)
    path('api/lugar/<int:lugar_id>/compartir/', views.registrar_compartido, name='registrar_compartido'),

    # Autenticación y Perfil de Usuario
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('perfil/', views.perfil, name='perfil'),

    # Panel Administrativo y Dashboard
    path('dashboard/', views.dashboard_municipal, name='dashboard_municipal'),
]
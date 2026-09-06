from .models import PerfilUsuario

def alerta_perfil(request):
    # 1. Filtro de Vistas: Si estamos en el panel de control o admin, apagamos el pop-up
    if request.path.startswith('/dashboard/') or request.path.startswith('/admin/'):
        return {'mostrar_alerta_perfil': False}

    mostrar = False
    
    # 2. Filtro de Usuario: Solo revisamos si inició sesión Y NO es del equipo municipal (staff)
    if request.user.is_authenticated and not request.user.is_staff:
        try:
            perfil = request.user.perfilusuario
            if perfil.intereses.count() == 0 or not perfil.edad:
                mostrar = True
        except PerfilUsuario.DoesNotExist:
            mostrar = True
            
    return {'mostrar_alerta_perfil': mostrar}
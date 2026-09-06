from django.shortcuts import render, get_object_or_404, redirect
from .models import Lugar, Categoria  # Importamos la tabla de lugares
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def index(request):
   # 1. Traemos todos los lugares y todas las categorías iniciales
    lugares_lista = Lugar.objects.all()
    categorias_lista = Categoria.objects.all()
    
    # 2. Capturamos lo que el usuario escribió o seleccionó (si es que lo hizo)
    busqueda = request.GET.get('buscar')
    categoria_id = request.GET.get('categoria')
    
    # 3. Aplicamos los filtros si hay datos
    if busqueda:
        # icontains busca palabras clave sin importar mayúsculas/minúsculas
        lugares_lista = lugares_lista.filter(nombre__icontains=busqueda)
        
    if categoria_id:
        # Filtramos por el ID de la categoría seleccionada
        lugares_lista = lugares_lista.filter(categoria_id=categoria_id)
        
    contexto = {
        'lugares': lugares_lista,
        'categorias': categorias_lista, # Enviamos las categorías al HTML
    }
    
    return render(request, 'index.html', contexto)
# NUEVA VISTA
def detalle_lugar(request, lugar_id):
    # Busca el lugar por su ID, si no existe, lanza error 404
    lugar = get_object_or_404(Lugar, id=lugar_id)
    contexto = {'lugar': lugar}
    return render(request, 'detalle.html', contexto)
# NUEVA VISTA: Registro de Usuarios
def registro(request):
    if request.method == 'POST':
        # Si el usuario envió sus datos, los procesamos
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save() # Guarda el usuario en la base de datos
            login(request, usuario) # Inicia sesión automáticamente
            return redirect('index') # Lo manda a la página principal
    else:
        # Si acaba de entrar a la página, le mostramos el formulario vacío
        form = UserCreationForm()
        
    contexto = {'form': form}
    return render(request, 'registro.html', contexto)
import os
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg, Count, F
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone

# Importamos modelos y motor de IA
from .models import Lugar, Categoria, PerfilUsuario, Resena, Evento
from .ml_engine import obtener_recomendaciones_rf

# PORTADA PÚBLICA
def landing(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'landing.html')

# HU02 / HU03 / HU05: Catálogo y Búsqueda
def index(request):
    lugares_lista = Lugar.objects.select_related('categoria').all()
    categorias_lista = Categoria.objects.all()
    
    busqueda = request.GET.get('buscar', '').strip()
    categoria_id = request.GET.get('categoria', '').strip()
    
    if busqueda:
        lugares_lista = lugares_lista.filter(nombre__icontains=busqueda)
        
    if categoria_id and categoria_id.isdigit():
        lugares_lista = lugares_lista.filter(categoria_id=int(categoria_id))
        
    recomendados_ids = [] 
    if request.user.is_authenticated and not request.user.is_staff:
        lugares_lista, recomendados_ids = obtener_recomendaciones_rf(request.user, lugares_lista)
        
    contexto = {
        'lugares': lugares_lista,
        'categorias': categorias_lista, 
        'recomendados_ids': recomendados_ids,
        'busqueda_actual': busqueda,
        'categoria_actual': int(categoria_id) if categoria_id.isdigit() else None
    }
    return render(request, 'index.html', contexto)

# HU03: Endpoint Asíncrono para Búsqueda y Filtrado (Fetch API)
def api_buscar_lugares(request):
    busqueda = request.GET.get('buscar', '').strip()
    categoria_id = request.GET.get('categoria', '').strip()
    
    lugares = Lugar.objects.select_related('categoria').all()
    if busqueda:
        lugares = lugares.filter(nombre__icontains=busqueda)
    if categoria_id and categoria_id.isdigit():
        lugares = lugares.filter(categoria_id=int(categoria_id))
        
    data = [{
        'id': l.id,
        'nombre': l.nombre,
        'descripcion': l.descripcion[:120] + '...',
        'categoria': l.categoria.nombre if l.categoria else 'General',
        'latitud': l.latitud,
        'longitud': l.longitud,
        'precio': float(l.precio),
        'imagen_url': l.imagen.url if l.imagen else ''
    } for l in lugares]
    
    return JsonResponse({'lugares': data, 'total': len(data)})

# HU04 / HU08: Detalle del Lugar y Reseñas
def detalle_lugar(request, lugar_id):
    lugar = get_object_or_404(Lugar, id=lugar_id)
    resenas = lugar.resenas.all().order_by('-fecha')

    if request.method == 'POST' and request.user.is_authenticated:
        comentario_texto = request.POST.get('comentario', '').strip()
        calificacion_num = request.POST.get('calificacion', '').strip()
        
        if comentario_texto and calificacion_num:
            palabras_prohibidas = ['insulto1', 'obsceno2']
            if any(palabra in comentario_texto.lower() for palabra in palabras_prohibidas):
                messages.error(request, "Tu comentario contiene palabras inapropiadas no permitidas en la plataforma.")
                return redirect('detalle_lugar', lugar_id=lugar.id)

            Resena.objects.create(
                lugar=lugar,
                usuario=request.user,
                calificacion=int(calificacion_num),
                comentario=comentario_texto
            )
            messages.success(request, "¡Tu reseña ha sido publicada exitosamente!")
            return redirect('detalle_lugar', lugar_id=lugar.id)

    contexto = {
        'lugar': lugar,
        'resenas': resenas
    }
    return render(request, 'detalle.html', contexto)

# HU09: Registro de Métrica al Compartir en Redes
def registrar_compartido(request, lugar_id):
    if request.method == 'POST':
        lugar = get_object_or_404(Lugar, id=lugar_id)
        Lugar.objects.filter(id=lugar.id).update(compartidos=F('compartidos') + 1)
        lugar.refresh_from_db()
        return JsonResponse({'status': 'ok', 'compartidos': lugar.compartidos})
    return JsonResponse({'status': 'invalid'}, status=400)

# HU07: Listado Público de Eventos
def eventos_publicos(request):
    ahora = timezone.now()
    eventos = Evento.objects.filter(estado='publicado', fecha_fin__gte=ahora).order_by('fecha_inicio')
    return render(request, 'eventos.html', {'eventos': eventos})

# HU07: Crear Evento (Gestor Municipal / Staff)
@staff_member_required
def evento_crear(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        categoria_id = request.POST.get('categoria')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        ubicacion = request.POST.get('ubicacion')
        
        if titulo and fecha_inicio and fecha_fin:
            Evento.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                categoria_id=categoria_id if categoria_id else None,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                ubicacion=ubicacion,
                creado_por=request.user
            )
            messages.success(request, "Evento registrado con éxito en la agenda municipal.")
            return redirect('eventos_publicos')
            
    return render(request, 'admin_evento_form.html', {'categorias': categorias})

# HU01: Registro de Usuarios
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        correo_ingresado = request.POST.get('email', '').strip()
        
        if correo_ingresado and User.objects.filter(email__iexact=correo_ingresado).exists():
            messages.error(request, "⚠️ El correo electrónico ya se encuentra registrado en Explora Pucusana.")
            return render(request, 'registro.html', {'form': form})
        
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.email = correo_ingresado
            usuario.save()
            PerfilUsuario.objects.create(usuario=usuario)
            login(request, usuario) 
            messages.success(request, f"¡Registro completado con éxito! Bienvenido(a), {usuario.username}.")
            return redirect('perfil') 
    else:
        form = UserCreationForm()
        
    return render(request, 'registro.html', {'form': form})

# HU06: Perfil e Intereses
@login_required 
def perfil(request):
    perfil_obj, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    todas_categorias = Categoria.objects.all()

    if request.method == 'POST':
        perfil_obj.edad = request.POST.get('edad') or None
        perfil_obj.nacionalidad = request.POST.get('nacionalidad', 'Peruano')
        intereses_seleccionados = request.POST.getlist('intereses') 
        perfil_obj.intereses.set(intereses_seleccionados) 
        perfil_obj.save()
        messages.success(request, "🎯 Preferencias actualizadas. El motor de Inteligencia Artificial ha reestructurado tu catálogo.")
        return redirect('index') 

    contexto = {
        'perfil': perfil_obj,
        'categorias': todas_categorias,
        'intereses_actuales': perfil_obj.intereses.values_list('id', flat=True)
    }
    return render(request, 'perfil.html', contexto)

# DASHBOARD MUNICIPAL
@staff_member_required 
def dashboard_municipal(request):
    categorias = Categoria.objects.annotate(total=Count('lugares'))
    nombres_categorias = [c.nombre for c in categorias]
    totales_categorias = [c.total for c in categorias]

    lugares_top = Lugar.objects.annotate(promedio=Avg('resenas__calificacion')).order_by('-promedio')[:5]
    nombres_lugares = [l.nombre for l in lugares_top]
    promedios_lugares = [float(l.promedio or 0) for l in lugares_top]

    contexto = {
        'nombres_categorias': nombres_categorias,
        'totales_categorias': totales_categorias,
        'nombres_lugares': nombres_lugares,
        'promedios_lugares': promedios_lugares,
    }
    return render(request, 'dashboard.html', contexto)

# MAPA INTERACTIVO
def mapa_turistico(request):
    lugares = Lugar.objects.all()
    return render(request, 'mapa.html', {'lugares': lugares})
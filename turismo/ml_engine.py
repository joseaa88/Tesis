import os
import joblib
from django.conf import settings

# 1. Rutas a los archivos .pkl que pegaste en la carpeta turismo/
BASE_DIR = settings.BASE_DIR
MODEL_PATH = os.path.join(BASE_DIR, 'turismo', 'modelo_pucusana.pkl')
ENCODER_PATH = os.path.join(BASE_DIR, 'turismo', 'codificadores_pucusana.pkl')

# Cargar el cerebro de la IA
try:
    modelo_rf = joblib.load(MODEL_PATH)
    codificadores = joblib.load(ENCODER_PATH)
    print("✅ [ÉXITO] ¡Cerebro de IA y codificadores cargados correctamente!")
except Exception as e:
    print(f"❌ [ERROR] No se pudo cargar la IA. Error: {e}")
    modelo_rf = None
    codificadores = None

# ========================================================
# 2. EL TRADUCTOR (El puente entre Excel y Django)
# ========================================================
MAPEO_EXCEL_A_DJANGO = {
    '1': 1,  # Ej: En Excel 1 es "Playa Ninfas", y en Django su ID es 1
    '2': 2,  
    '3': 3,
    '4': 4,
    '303': 1, # Agregamos la predicción de la IA y la enlazamos a un lugar real de tu Django
    '215': 2, # Cuando la IA diga 215, mostramos el lugar con ID 2 en Django
    # Agrega más si tu base de datos tiene más IDs
}

def obtener_recomendaciones_rf(usuario, lugares_queryset):
    """
    Predice el lugar ideal para el usuario usando Random Forest y lo pone primero.
    """
    if not modelo_rf or not codificadores or not hasattr(usuario, 'perfilusuario'):
        print("⚠️ [AVISO] IA apagada o el usuario no tiene perfil. Mostrando catálogo normal.")
        return lugares_queryset, []

    perfil = usuario.perfilusuario
    
    # 3. Preparar los datos del turista
    edad = perfil.edad or 30
    procedencia = perfil.nacionalidad or 'Peruano'
    genero = 'Hombre'
    motivo = 'Turismo'

    try:
        gen_encoded = codificadores['genero'].transform([genero])[0]
        proc_encoded = codificadores['procedencia'].transform([procedencia])[0]
        mot_encoded = codificadores['motivo'].transform([motivo])[0]
    except ValueError:
        gen_encoded, proc_encoded, mot_encoded = 0, 0, 0

    # 4. LA PREDICCIÓN
    datos_usuario = [[edad, gen_encoded, proc_encoded, mot_encoded]]
    prediccion_excel = str(modelo_rf.predict(datos_usuario)[0])
    
    print(f"🤖 [DEBUG IA] La IA predijo el número del Excel: {prediccion_excel}")

    # 5. LA TRADUCCIÓN
    id_django_recomendado = MAPEO_EXCEL_A_DJANGO.get(prediccion_excel, None)
    print(f"🔄 [DEBUG TRADUCCIÓN] Se tradujo al ID de Django: {id_django_recomendado}")

    # 6. Reordenar el Catálogo Visual
    lugares_ordenados = list(lugares_queryset)
    recomendados_ids = []

    if id_django_recomendado:
        for lugar in lugares_ordenados:
            if lugar.id == id_django_recomendado:
                lugares_ordenados.remove(lugar)
                lugares_ordenados.insert(0, lugar) # Lo ponemos primero
                recomendados_ids.append(lugar.id)  # Etiqueta de Recomendado
                break

    return lugares_ordenados, recomendados_ids
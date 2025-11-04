# web/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SolicitudRegistroForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.conf import settings
import os

def home_view(request):
    return render(request, 'home.html')

def handle_not_found_view(request):
    """
    Vista personalizada para manejar errores 404 (página no encontrada).
    Renderiza un template amigable en lugar de la página de error por defecto de Django.
    """
    response = render(request, '404.html', {})
    response.status_code = 404
    return response

"""def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard') 

    if request.method == 'POST':
        form = RegistroConCodigoForm(request.POST)
        if form.is_valid():
            user = form.save() # La lógica de creación está ahora en el formulario
        # 1. Inicia sesión automáticamente para el nuevo usuario
            login(request, user)
            
            # 2. Muestra un mensaje de bienvenida
            messages.success(request, f'¡Bienvenido, {user.username}! Tu cuenta ha sido creada exitosamente.')
            
            # 3. Redirige al dashboard en lugar de al login
            return redirect('dashboard')
            
            # --- FIN DE LA MODIFICACIÓN ---
    else:
        form = RegistroConCodigoForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)

def crear_superusuario_secreto(request):
    # --- ACCESO SEGURO A VARIABLES DE ENTORNO ---
    # Usamos os.environ.get() que devuelve None si la variable no existe, en lugar de crashear.
    superuser_secret_key = os.environ.get('SECRET_KEY_SUPERUSER')
    
    # 1. Verificación de seguridad principal
    if settings.DEBUG or not superuser_secret_key:
        return HttpResponse("Acción no permitida (DEBUG o clave no configurada).", status=403)

    # 2. Obtenemos la clave de la URL
    provided_key = request.GET.get('key', '')
    if provided_key != superuser_secret_key:
        # Damos un mensaje más claro para depurar
        return HttpResponse(f"Clave incorrecta. Provista: '{provided_key}', Esperada: '{superuser_secret_key}'", status=403)

    # --- LÓGICA DE CREACIÓN (sin cambios) ---
    User = get_user_model()
    username = 'super'
    email = 'super@example.com'
    password = 'super' # Recuerda cambiar esta contraseña después de iniciar sesión

    if not User.objects.filter(username=username).exists():
        try:
            User.objects.create_superuser(username, email, password)
            return HttpResponse(f"¡Superusuario '{username}' creado exitosamente! Ya puedes iniciar sesión.")
        except Exception as e:
            # Si hay un error al crear (ej. la base de datos no está), ahora lo veremos.
            return HttpResponse(f"Error al crear el superusuario: {e}", status=500)
    else:
        return HttpResponse(f"El superusuario '{username}' ya existe.") """

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard') 

    if request.method == 'POST':
        form = SolicitudRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Solicitud Enviada|Tu solicitud de registro ha sido enviada y está pendiente de aprobación.')
            return redirect('login') # Lo enviamos al login
    else:
        form = SolicitudRegistroForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)
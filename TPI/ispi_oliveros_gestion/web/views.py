# web/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroConCodigoForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.conf import settings

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

def register_view(request):
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
    # --- ¡MÁXIMA SEGURIDAD! ---
    # Esta vista solo funcionará si estamos en modo DEBUG=False (producción)
    # y si hemos definido una contraseña secreta en las variables de entorno.
    # Esto evita que cualquiera pueda ejecutarla.
    
    if settings.DEBUG or not settings.SECRET_KEY_SUPERUSER:
        return HttpResponse("Acción no permitida.", status=403)

    # Obtenemos la contraseña de la URL, ej: /url-secreta/12345/
    provided_key = request.GET.get('key', '')
    if provided_key != settings.SECRET_KEY_SUPERUSER:
        return HttpResponse("Clave incorrecta.", status=403)

    # --- LÓGICA DE CREACIÓN ---
    User = get_user_model()
    username = 'super'
    email = 'super@example.com'
    password = 'super'

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        return HttpResponse(f"¡Superusuario '{username}' creado exitosamente! Ya puedes iniciar sesión.")
    else:
        return HttpResponse(f"El superusuario '{username}' ya existe.")
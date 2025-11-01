# web/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroConCodigoForm
from django.contrib.auth import login

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
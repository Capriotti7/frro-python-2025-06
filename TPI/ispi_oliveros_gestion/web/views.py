# web/views.py

from django.shortcuts import render

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
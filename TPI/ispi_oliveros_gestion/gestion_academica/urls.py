from django.contrib import admin
from django.urls import path, include, re_path
from web.views import home_view, handle_not_found_view, register_view
from web.views import crear_superusuario_secreto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'), # La página pública

    
    path('accounts/register/', register_view, name='register'),
    # 1. URLs de Autenticación (login, logout, etc.)
    # Django nos da esto ya hecho.
    path('accounts/', include('django.contrib.auth.urls')),

    # 2. URLs de nuestra app principal de gestión
    path('gestion/', include('core.urls')),
    path('gestion/alumnos/', include('alumnos.urls')),
    path('gestion/academico/', include('academico.urls')),
    path('gestion/finanzas/', include('finanzas.urls')),

    # 3. Manejo de errores 404 con una vista personalizada
    re_path(r'^.*$', handle_not_found_view, name='catch_all'),

    # --- URL SECRETA PARA CREAR SUPERUSUARIO ---
    # Usa un nombre largo y difícil de adivinar.
    path('crear-primer-superusuario-render-9xyz789/', crear_superusuario_secreto, name='crear_su_secreto'),
]

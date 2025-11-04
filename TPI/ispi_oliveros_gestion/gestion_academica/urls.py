from django.contrib import admin
from django.urls import path, include, re_path
from web.views import home_view, handle_not_found_view, register_view, crear_superusuario_secreto

urlpatterns = [
    # 1. Rutas principales de la aplicación
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),

    # 2. Rutas de autenticación (Agrupadas)
    # Primero definimos nuestra ruta de registro personalizada
    path('accounts/register/', register_view, name='register'),
    # Luego, incluimos el resto de las URLs de autenticación de Django
    path('accounts/', include('django.contrib.auth.urls')),

    # 3. Rutas de los módulos de gestión
    path('gestion/', include('core.urls')),
    path('gestion/alumnos/', include('alumnos.urls')),
    path('gestion/academico/', include('academico.urls')),
    path('gestion/finanzas/', include('finanzas.urls')),

    # 4. UURL SECRETA PARA CREAR SUPERUSUARIO
    path('crear-primer-superusuario-render-9xyz789/', crear_superusuario_secreto, name='crear_su_secreto'),

    # 5. El "Atrapa-Todo" para 404
    re_path(r'^.*$', handle_not_found_view, name='catch_all'),
]

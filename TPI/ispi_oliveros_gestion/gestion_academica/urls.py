from django.contrib import admin
from django.urls import path, include
from web.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'), # La página pública

    # 1. URLs de Autenticación (login, logout, etc.)
    # Django nos da esto ya hecho.
    path('accounts/', include('django.contrib.auth.urls')),

    # 2. URLs de nuestra app principal de gestión
    path('gestion/', include('core.urls')),
    path('gestion/alumnos/', include('alumnos.urls')),
    path('gestion/academico/', include('academico.urls')),
]
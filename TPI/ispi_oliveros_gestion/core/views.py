# core/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from alumnos.models import Alumno # Importar modelos
from academico.models import Carrera

@login_required
def dashboard(request):
    user = request.user
    
    # Si eres Superusuario, ves el dashboard original con todas las estadísticas
    if user.is_superuser:
        alumnos_count = Alumno.objects.count()
        carreras_count = Carrera.objects.count()
        context = {
            'user': user,
            'alumnos_count': alumnos_count,
            'carreras_count': carreras_count,
        }
        return render(request, 'core/dashboard.html', context)
    
    # Si tienes perfil de Administrador, ves un dashboard simplificado
    elif hasattr(user, 'perfil_administrador'):
        context = {'user': user}
        return render(request, 'core/dashboard_administrativo.html', context)

    # Si tienes perfil de Docente (lo haremos en el futuro)
    elif hasattr(user, 'perfil_docente'):
        # Por ahora, un dashboard simple para docentes
        context = {'user': user}
        return render(request, 'core/dashboard_docente.html', context)

    # Si no es ninguno, una página genérica
    else:
        return render(request, 'core/dashboard_general.html', {})
# core/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from alumnos.models import Alumno # Importar modelos
from academico.models import Carrera

@login_required
def dashboard(request):
    alumnos_count = Alumno.objects.count()
    carreras_count = Carrera.objects.count()
    # En el futuro: docentes_count, cursos_activos, etc.

    context = {
        'user': request.user,
        'alumnos_count': alumnos_count,
        'carreras_count': carreras_count,
    }
    return render(request, 'core/dashboard.html', context)
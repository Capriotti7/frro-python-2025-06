# core/views.py

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from alumnos.models import Alumno
from academico.models import Carrera, Docente

from django.contrib.auth.models import User
from .models import Administrador, SolicitudRegistro
from .decorators import role_required

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


# Gestión de Solicitudes de Registro
@login_required
@role_required('is_superuser')
def gestion_solicitudes_view(request):
    solicitudes_pendientes = SolicitudRegistro.objects.filter(estado='PENDIENTE')
    context = {'solicitudes': solicitudes_pendientes}
    return render(request, 'core/gestion_solicitudes.html', context)

@login_required
@role_required('is_superuser')
def aprobar_solicitud_view(request, solicitud_pk):
    solicitud = get_object_or_404(SolicitudRegistro, pk=solicitud_pk)
    
    # Crear el User
    user = User.objects.create_user(
        username=solicitud.username,
        email=solicitud.email,
        first_name=solicitud.first_name,
        last_name=solicitud.last_name
    )
    user.password = solicitud.password_hash # Asignamos el hash guardado
    user.save()

    # Crear el Perfil correspondiente
    if solicitud.tipo_perfil == 'ADMIN':
        Administrador.objects.create(user=user)
    elif solicitud.tipo_perfil == 'DOCENTE':
        Docente.objects.create(
            user=user,
            dni=solicitud.dni,
            telefono=solicitud.telefono
        )
    
    solicitud.estado = 'APROBADO'
    solicitud.save()
    
    messages.success(request, f'Éxito|La solicitud de {user.username} ha sido aprobada.')
    return redirect('gestion_solicitudes')

@login_required
@role_required('is_superuser')
def rechazar_solicitud_view(request, solicitud_pk):
    solicitud = get_object_or_404(SolicitudRegistro, pk=solicitud_pk)
    solicitud.estado = 'RECHAZADO'
    solicitud.save()
    messages.success(request, f'Solicitud Rechazada|La solicitud de {solicitud.username} ha sido rechazada.')
    return redirect('gestion_solicitudes')
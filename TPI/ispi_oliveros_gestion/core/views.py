# core/views.py

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from alumnos.models import Alumno
from academico.models import Carrera, Docente, InscripcionCurso
from django.db.models import Count, Max, Min, Q

from django.contrib.auth.models import User
from .models import Administrador, SolicitudRegistro
from .decorators import role_required

def calcular_promedio_carrera():
    aprobaciones = InscripcionCurso.objects.filter(Q(nota_final__gte=6) | Q(condicion='Promocionado'))
    tiempos = []
    
    alumnos = Alumno.objects.all()
    carreras = Carrera.objects.annotate(num_materias=Count('materias'))
    
    for alumno in alumnos:
        for carrera in carreras:
            if carrera.num_materias == 0:
                continue
            
            insc_aprobadas = aprobaciones.filter(alumno=alumno, curso__materia__carrera=carrera)
            materias_aprobadas_ids = insc_aprobadas.values_list('curso__materia_id', flat=True).distinct()
            
            if len(materias_aprobadas_ids) == carrera.num_materias:
                insc_todas = InscripcionCurso.objects.filter(alumno=alumno, curso__materia__carrera=carrera)
                primera_insc = insc_todas.aggregate(Min('fecha_inscripcion'))['fecha_inscripcion__min']
                ultima_aprob = insc_aprobadas.aggregate(Max('fecha_inscripcion'))['fecha_inscripcion__max']
                
                if primera_insc and ultima_aprob:
                    diferencia = ultima_aprob - primera_insc
                    tiempos.append(diferencia.days / 365.25)
    
    if tiempos:
        return sum(tiempos) / len(tiempos)
    return None

@login_required
def dashboard(request):
    user = request.user
    
    # Si eres Superusuario, ves el dashboard original con todas las estadÃ­sticas
    if user.is_superuser:
        alumnos_count = Alumno.objects.count()
        carreras_count = Carrera.objects.count()
        promedio_anios = calcular_promedio_carrera()

        if promedio_anios is not None:
            promedio_str = f"{promedio_anios:.1f} años"
        else:
            promedio_str = "N/A"

        context = {
            'user': user,
            'alumnos_count': alumnos_count,
            'carreras_count': carreras_count,
            'tiempo_promedio_carrera': promedio_str,
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

    # Si no es ninguno, una pÃ¡gina genÃ©rica
    else:
        return render(request, 'core/dashboard_general.html', {})


# GestiÃ³n de Solicitudes de Registro
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

# --- CRUD DE ADMINISTRADORES ---
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from .forms import AdministradorForm

@method_decorator([login_required, role_required('is_superuser')], name='dispatch')
class AdministradorListView(ListView):
    model = Administrador
    template_name = 'core/administrador/list.html'
    context_object_name = 'administradores'

@method_decorator([login_required, role_required('is_superuser')], name='dispatch')
class AdministradorCreateView(CreateView):
    model = Administrador
    form_class = AdministradorForm
    template_name = 'core/administrador/form.html'
    success_url = reverse_lazy('administrador_list')

    def form_valid(self, form):
        messages.success(self.request, "Éxito|Administrador creado correctamente.")
        return super().form_valid(form)

@method_decorator([login_required, role_required('is_superuser')], name='dispatch')
class AdministradorUpdateView(UpdateView):
    model = Administrador
    form_class = AdministradorForm
    template_name = 'core/administrador/form.html'
    success_url = reverse_lazy('administrador_list')

    def form_valid(self, form):
        messages.success(self.request, "Éxito|Administrador actualizado correctamente.")
        return super().form_valid(form)

@method_decorator([login_required, role_required('is_superuser')], name='dispatch')
class AdministradorDeleteView(DeleteView):
    model = Administrador
    template_name = 'core/administrador/confirm_delete.html'
    success_url = reverse_lazy('administrador_list')

    def delete(self, request, *args, **kwargs):
        admin = self.get_object()
        user = admin.user
        response = super().delete(request, *args, **kwargs)
        # Eliminamos en cascada tambiÃ©n el User correspondiente de auth_user
        user.delete()
        messages.success(self.request, "Éxito|Administrador eliminado correctamente.")
        return response

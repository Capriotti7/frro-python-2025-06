# academico/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from alumnos.models import Alumno
from .models import Carrera, Materia, Curso, InscripcionCurso, Asistencia
from django.utils import timezone
from .forms import CarreraForm, MateriaForm, CursoForm, DocenteForm
from django.db.models import Q
from django.views.decorators.http import require_POST
from core.decorators import role_required
from core.models import Docente


# --- VISTAS PARA CARRERA ---
@login_required
def carrera_list_view(request):
    carreras = Carrera.objects.all().order_by('nombre')
    context = {'carreras': carreras}
    return render(request, 'academico/carrera/list.html', context)

@role_required('is_superuser')
@login_required
def carrera_create_view(request):
    if request.method == 'POST':
        form = CarreraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'La carrera ha sido creada exitosamente.')
            return redirect('academico:carrera_list')
    else:
        form = CarreraForm()
    context = {'form': form}
    return render(request, 'academico/carrera/form.html', context)

@role_required('is_superuser')
@login_required
def carrera_update_view(request, pk):
    carrera = get_object_or_404(Carrera, pk=pk)
    if request.method == 'POST':
        form = CarreraForm(request.POST, instance=carrera)
        if form.is_valid():
            form.save()
            messages.success(request, 'La carrera ha sido actualizada exitosamente.')
            return redirect('academico:carrera_list')
    else:
        form = CarreraForm(instance=carrera)
    context = {'form': form, 'carrera': carrera}
    return render(request, 'academico/carrera/form.html', context)

@role_required('is_superuser')
@login_required
def carrera_delete_view(request, pk):
    carrera = get_object_or_404(Carrera, pk=pk)
    if request.method == 'POST':
        carrera.delete()
        messages.success(request, 'La carrera ha sido eliminada.')
        return redirect('academico:carrera_list')
    context = {'carrera': carrera}
    return render(request, 'academico/carrera/confirm_delete.html', context)

# --- VISTAS PARA MATERIA ---
@login_required
def materia_list_view(request, carrera_pk):
    carrera = get_object_or_404(Carrera, pk=carrera_pk)
    materias = Materia.objects.filter(carrera=carrera).order_by('anio_carrera', 'nombre')
    context = {'carrera': carrera, 'materias': materias}
    return render(request, 'academico/materia/list.html', context)

@role_required('is_superuser')
@login_required
def materia_create_view(request, carrera_pk):
    carrera = get_object_or_404(Carrera, pk=carrera_pk)
    if request.method == 'POST':
        form = MateriaForm(request.POST, carrera=carrera)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.carrera = carrera
            materia.save()
            messages.success(request, 'La materia ha sido creada exitosamente.')
            return redirect('academico:materia_list', carrera_pk=carrera.pk)
    else:
        form = MateriaForm(carrera=carrera)
    
    context = {'form': form, 'carrera': carrera}
    return render(request, 'academico/materia/form.html', context)

@role_required('is_superuser')
@login_required
def materia_update_view(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    carrera = materia.carrera
    if request.method == 'POST':
        form = MateriaForm(request.POST, instance=materia, carrera=carrera)
        if form.is_valid():
            form.save()
            messages.success(request, 'La materia ha sido actualizada exitosamente.')
            return redirect('academico:materia_list', carrera_pk=carrera.pk)
    else:
        form = MateriaForm(instance=materia, carrera=carrera)
        
    context = {'form': form, 'carrera': carrera}
    return render(request, 'academico/materia/form.html', context)

@role_required('is_superuser')
@login_required
def materia_delete_view(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    if request.method == 'POST':
        carrera_pk = materia.carrera.pk
        materia.delete()
        messages.success(request, 'La materia ha sido eliminada.')
        return redirect('academico:materia_list', carrera_pk=carrera_pk)
    context = {'materia': materia}
    return render(request, 'academico/materia/confirm_delete.html', context)

# --- VISTAS PARA CURSO ---
@login_required
def curso_list_view(request, materia_pk):
    materia = get_object_or_404(Materia, pk=materia_pk)
    cursos = Curso.objects.filter(materia=materia).order_by('-ciclo_lectivo', 'cuatrimestre')
    docentes_disponibles = Docente.objects.all().order_by('apellido', 'nombre')
    context = {
        'materia': materia,
        'cursos': cursos,
        'docentes_disponibles': docentes_disponibles,}
    return render(request, 'academico/curso/list.html', context)


@login_required
@role_required('is_superuser', 'is_admin')
def curso_create_view(request, materia_pk):
    materia = get_object_or_404(Materia, pk=materia_pk)
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.materia = materia
            curso.save()
            messages.success(request, 'El curso ha sido creado exitosamente.')
            return redirect('academico:curso_list', materia_pk=materia.pk)
    else:
        form = CursoForm()
    context = {'form': form, 'materia': materia}
    return render(request, 'academico/curso/form.html', context)

@login_required
@role_required('is_superuser', 'is_admin')
def curso_update_view(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, 'El curso ha sido actualizado exitosamente.')
            return redirect('academico:curso_list', materia_pk=curso.materia.pk)
    else:
        form = CursoForm(instance=curso)
    context = {'form': form, 'materia': curso.materia}
    return render(request, 'academico/curso/form.html', context)

@login_required
@role_required('is_superuser', 'is_admin')
def curso_delete_view(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        materia_pk = curso.materia.pk
        curso.delete()
        messages.success(request, 'El curso ha sido eliminado.')
        return redirect('academico:curso_list', materia_pk=materia_pk)
    context = {'curso': curso}
    return render(request, 'academico/curso/confirm_delete.html', context)

# --- VISTAS PARA DOCENTE ---
@login_required
@role_required('is_superuser', 'is_admin')
def docente_list_view(request):
    docentes = Docente.objects.all().order_by('apellido', 'nombre')
    context = {'docentes': docentes}
    materia_id = request.GET.get('from_materia')
    if materia_id:
        try:
            # Buscamos la materia y la añadimos al contexto
            materia_origen = get_object_or_404(Materia, pk=materia_id)
            context['materia_origen'] = materia_origen
        except (ValueError, TypeError):
            # Si el ID no es válido, simplemente no hacemos nada
            pass
    return render(request, 'academico/docente/list.html', context)

@login_required
@role_required('is_superuser', 'is_admin')
def docente_list_from_materia_view(request, materia_pk):
    # 1. Obtenemos la materia desde la que venimos, gracias a la URL
    materia = get_object_or_404(Materia, pk=materia_pk)
    
    # 2. Obtenemos la lista de TODOS los docentes del sistema
    docentes = Docente.objects.all().order_by('apellido', 'nombre')
    
    # 3. Preparamos y enviamos los datos a una NUEVA plantilla
    context = {
        'materia': materia,
        'docentes': docentes
    }
    return render(request, 'academico/docente/list_from_materia.html', context)


@login_required
@role_required('is_superuser', 'is_admin')
def docente_create_view(request):
    # Leemos la "pista" de la URL, tanto si es GET (al cargar) como si es POST (al enviar)
    materia_pk_origen = request.POST.get('from_materia') or request.GET.get('from_materia')

    if request.method == 'POST':
        form = DocenteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El docente ha sido agregado exitosamente.')

            # Si teníamos la "pista", volvemos a la lista de docentes de esa materia
            if materia_pk_origen:
                return redirect('academico:docente_list_from_materia', materia_pk=materia_pk_origen)
            else:
                # Si no, volvemos a la lista general (comportamiento original)
                return redirect('academico:docente_list')
    else:
        form = DocenteForm()
        
    context = {
        'form': form,
        'materia_pk_origen': materia_pk_origen, # Pasamos la "pista" a la plantilla del formulario
    }
    return render(request, 'academico/docente/form.html', context)

@login_required
@role_required('is_superuser', 'is_admin')
def docente_update_view(request, pk):
    docente = get_object_or_404(Docente, pk=pk)
    if request.method == 'POST':
        form = DocenteForm(request.POST, instance=docente)
        if form.is_valid():
            form.save()
            messages.success(request, 'El docente ha sido actualizado exitosamente.')
            return redirect('academico:docente_list')
    else:
        form = DocenteForm(instance=docente)
    context = {'form': form, 'docente': docente}
    return render(request, 'academico/docente/form.html', context)

@login_required
@role_required('is_superuser', 'is_admin')
def docente_delete_view(request, pk):
    docente = get_object_or_404(Docente, pk=pk)
    if request.method == 'POST':
        docente.delete()
        messages.success(request, 'El docente ha sido eliminado.')
        return redirect('academico:docente_list')
    context = {'docente': docente}
    return render(request, 'academico/docente/confirm_delete.html', context)

@login_required
@role_required('is_superuser', 'is_admin')
def docente_delete_from_materia_view(request, pk, materia_pk):
    docente = get_object_or_404(Docente, pk=pk)
    materia = get_object_or_404(Materia, pk=materia_pk) # También obtenemos la materia

    if request.method == 'POST':
        docente.delete()
        messages.success(request, 'El docente ha sido eliminado.')
        # ¡LA LÍNEA CLAVE! Redirige de vuelta a la lista de docentes de la materia
        return redirect('academico:docente_list_from_materia', materia_pk=materia.pk)
    
    context = {
        'docente': docente,
        'materia': materia  # Pasamos la materia a la plantilla de confirmación
    }
    # Reutilizamos la misma plantilla de confirmación
    return render(request, 'academico/docente/confirm_delete.html', context)

# --- VISTAS PARA INSCRIPCIONES A CURSOS ---
@login_required
@role_required('is_superuser', 'is_admin')
def curso_selection_list_view(request, alumno_pk):
    alumno = get_object_or_404(Alumno, pk=alumno_pk)
    
    # Obtenemos los IDs de los cursos en los que el alumno YA está inscripto.
    cursos_inscrito_ids = InscripcionCurso.objects.filter(alumno=alumno).values_list('curso__id', flat=True)
    
    # Obtenemos todos los cursos disponibles, EXCLUYENDO aquellos en los que ya está inscripto.
    cursos_disponibles = Curso.objects.exclude(id__in=cursos_inscrito_ids).order_by('-ciclo_lectivo', 'materia__nombre')
    
    context = {
        'alumno': alumno,
        'cursos': cursos_disponibles,
    }
    return render(request, 'academico/inscripcion/curso_selection_list.html', context)

@login_required
@role_required('is_superuser', 'is_admin')
def inscribir_alumno_ejecutar_view(request):
    if request.method == 'POST':
        alumno_pk = request.POST.get('alumno_pk')
        curso_pk = request.POST.get('curso_pk')
        
        alumno = get_object_or_404(Alumno, pk=alumno_pk)
        curso = get_object_or_404(Curso, pk=curso_pk)
        
        # Regla de Negocio: Verificar si ya existe la inscripción
        if InscripcionCurso.objects.filter(alumno=alumno, curso=curso).exists():
            messages.error(request, f'Error|El alumno ya se encuentra inscripto en el curso de {curso.materia.nombre}.')
        else:
            InscripcionCurso.objects.create(alumno=alumno, curso=curso)
            messages.success(request, f'Inscripción Exitosa|Se ha inscripto a {alumno.apellido}, {alumno.nombre} en el curso de {curso.materia.nombre}.')
            
        return redirect('alumnos:alumno_detail', pk=alumno.pk)
    
    # Si no es POST, redirigir a algún lugar seguro, como el dashboard.
    return redirect('dashboard')

# --- VISTAS PARA GESTIÓN DE ASISTENCIAS ---
@login_required
def gestionar_asistencias_view(request, curso_pk):
    curso = get_object_or_404(Curso, pk=curso_pk)
    
    # Obtener la fecha de la URL (si se proveyó) o usar la de hoy
    fecha_str = request.GET.get('fecha', timezone.now().strftime('%Y-%m-%d'))
    fecha = timezone.datetime.strptime(fecha_str, '%Y-%m-%d').date()

    if request.method == 'POST':
        # --- LÓGICA DE GUARDADO ---
        for inscripcion in curso.inscripciones.all():
            estado = request.POST.get(f'asistencia-{inscripcion.pk}')
            if estado:
                # update_or_create: busca una asistencia para este día/inscripción
                # si la encuentra, la actualiza; si no, la crea. ¡Mágico!
                Asistencia.objects.update_or_create(
                    inscripcion=inscripcion,
                    fecha_clase=fecha,
                    defaults={'estado': estado}
                )
        messages.success(request, f'Guardado|Se guardó la asistencia para el día {fecha.strftime("%d/%m/%Y")}.')
        return redirect('academico:gestionar_asistencias', curso_pk=curso.pk)

    # --- LÓGICA DE CARGA DE PÁGINA ---
    inscripciones = curso.inscripciones.all().select_related('alumno').order_by('alumno__apellido', 'alumno__nombre')
    
    # Obtenemos las asistencias ya guardadas para este día para pre-marcar los botones
    asistencias_del_dia = Asistencia.objects.filter(inscripcion__in=inscripciones, fecha_clase=fecha)
    
    # Creamos un diccionario para buscar fácilmente el estado de cada alumno en el template
    estado_asistencia = {asistencia.inscripcion.pk: asistencia.estado for asistencia in asistencias_del_dia}
    
    context = {
        'curso': curso,
        'inscripciones': inscripciones,
        'fecha': fecha,
        'estado_asistencia': estado_asistencia,
    }
    return render(request, 'academico/asistencia/gestionar.html', context)

@login_required
def asistencia_seleccion_curso_view(request):
    # En el futuro, si un docente inicia sesión, podríamos mostrar solo SUS cursos.
    # if request.user.groups.filter(name='Docentes').exists():
    #     cursos = Curso.objects.filter(docente=request.user.docente_profile)
    # else:
    #     cursos = Curso.objects.all()
    
    # Por ahora, mostramos todos los cursos del ciclo lectivo actual.
    current_year = timezone.now().year
    cursos = Curso.objects.filter(ciclo_lectivo=current_year).order_by('materia__nombre')
    
    context = {
        'cursos': cursos,
    }
    return render(request, 'academico/asistencia/seleccion_curso.html', context)

# --- VISTA PARA VER HISTORIAL DE ASISTENCIAS ---
@login_required
def ver_asistencias_view(request, inscripcion_pk):
    inscripcion = get_object_or_404(InscripcionCurso, pk=inscripcion_pk)
    asistencias = Asistencia.objects.filter(inscripcion=inscripcion).order_by('fecha_clase')
    
    # --- Cálculos para el Resumen ---
    total_clases = asistencias.count()
    presentes = asistencias.filter(estado='Presente').count()
    ausentes = asistencias.filter(estado='Ausente').count()
    justificados = asistencias.filter(estado='Justificado').count()
    
    # Calculamos el porcentaje de asistencia (evitando división por cero)
    porcentaje_asistencia = (presentes / total_clases * 100) if total_clases > 0 else 0
    
    context = {
        'inscripcion': inscripcion,
        'asistencias': asistencias,
        'total_clases': total_clases,
        'presentes': presentes,
        'ausentes': ausentes,
        'justificados': justificados,
        'porcentaje_asistencia': porcentaje_asistencia,
    }
    return render(request, 'academico/asistencia/ver_historial.html', context)

@login_required
def curso_detail_view(request, curso_pk):
    curso = get_object_or_404(Curso, pk=curso_pk)
    # Buscamos todas las inscripciones para este curso
    inscripciones = InscripcionCurso.objects.filter(curso=curso).order_by('alumno__apellido', 'alumno__nombre')
    
    context = {
        'curso': curso,
        'inscripciones': inscripciones
    }
    return render(request, 'academico/curso/detail.html', context)


@login_required
@role_required('is_superuser', 'is_admin')
def curso_inscribir_alumno_list_view(request, curso_pk):
    curso = get_object_or_404(Curso, pk=curso_pk)

    # 1. Obtener los IDs de los alumnos que YA están inscriptos en este curso
    alumnos_inscriptos_ids = InscripcionCurso.objects.filter(curso=curso).values_list('alumno_id', flat=True)

    # 2. Obtener todos los alumnos EXCLUYENDO a los que ya están inscriptos
    alumnos_disponibles = Alumno.objects.exclude(id__in=alumnos_inscriptos_ids)

    # 3. Lógica de Búsqueda por DNI
    search_dni = request.GET.get('dni_search', '') # '' es el valor por defecto
    if search_dni:
        alumnos_disponibles = alumnos_disponibles.filter(dni__icontains=search_dni)

    context = {
        'curso': curso,
        'alumnos': alumnos_disponibles,
        'search_dni': search_dni, # Para mantener el valor en la barra de búsqueda
    }
    return render(request, 'academico/curso/inscribir_list.html', context)

@require_POST # Asegura que esta vista solo se pueda llamar con un método POST
@login_required
@role_required('is_superuser', 'is_admin')
def curso_inscribir_alumno_action_view(request, curso_pk, alumno_pk):
    curso = get_object_or_404(Curso, pk=curso_pk)
    alumno = get_object_or_404(Alumno, pk=alumno_pk)

    # Usamos get_or_create para evitar inscribir al mismo alumno dos veces.
    # Si ya existe, no hace nada. Si no existe, lo crea.
    inscripcion, created = InscripcionCurso.objects.get_or_create(
        curso=curso,
        alumno=alumno
    )

    if created:
        messages.success(request, f'El alumno {alumno} ha sido inscripto exitosamente.')
    else:
        messages.warning(request, f'El alumno {alumno} ya se encontraba inscripto en este curso.')

    # Redirigimos de vuelta a la página de búsqueda e inscripción
    return redirect('academico:curso_inscribir_alumno_list', curso_pk=curso.pk)
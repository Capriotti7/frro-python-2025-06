# alumnos/views.py

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.decorators import role_required
from .models import Alumno 
from .forms import AlumnoForm
from finanzas.models import Deuda
from academico.models import InscripcionCurso
from django.db.models import Q

@login_required
@role_required('is_superuser', 'is_admin')
def alumno_list_view(request):
    # Obtenemos el término de búsqueda de la URL (?q=...)
    query = request.GET.get('q', '')
    
    # Empezamos con todos los alumnos
    alumnos_list = Alumno.objects.all()
    
    # Si hay un término de búsqueda, filtramos el queryset
    if query:
        alumnos_list = alumnos_list.filter(
            Q(apellido__icontains=query) | 
            Q(nombre__icontains=query) | 
            Q(dni__icontains=query)
        )
    
    # Finalmente, ordenamos el resultado
    alumnos = alumnos_list.order_by('apellido', 'nombre')
    
    context = {
        'alumnos': alumnos,
        'query': query, # Pasamos el query al template para que se mantenga en la barra
    }
    return render(request, 'alumnos/alumno/list.html', context)

@login_required
@role_required('is_superuser', 'is_admin')
def alumno_create_view(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'El alumno {form.cleaned_data["apellido"]}, {form.cleaned_data["nombre"]} ha sido agregado exitosamente.')
            return redirect('alumnos:alumno_list')
    else:
        form = AlumnoForm()

    context = {
        'form': form
    }
    return render(request, 'alumnos/alumno/form.html', context)

@login_required
@role_required('is_superuser', 'is_admin')
def alumno_update_view(request, pk):

    alumno = get_object_or_404(Alumno, pk=pk)

    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            messages.success(request, f'El alumno {alumno.apellido}, {alumno.nombre} ha sido actualizado exitosamente.')
            return redirect('alumnos:alumno_list')
    else:
        form = AlumnoForm(instance=alumno)

    context = {
        'form': form,
        'alumno': alumno
    }
    return render(request, 'alumnos/alumno/form.html', context)

@login_required
@role_required('is_superuser', 'is_admin')
def alumno_delete_view(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)

    if request.method == 'POST':
        nombre_completo = f'{alumno.apellido}, {alumno.nombre}'
        alumno.delete()
        messages.success(request, f'El alumno {nombre_completo} ha sido eliminado.')
        return redirect('alumnos:alumno_list')

    context = {
        'alumno': alumno
    }
    return render(request, 'alumnos/alumno/confirm_delete.html', context)

@login_required
@role_required('is_superuser', 'is_admin')
def alumno_detail_view(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)

    # --- LÓGICA FINANCIERA ---
    deudas = Deuda.objects.filter(alumno=alumno).order_by('-fecha_vencimiento')

    total_adeudado_calculado = 0
    total_pagado_calculado = 0
    
    for d in deudas:
        # Sumamos lo que se ha pagado por cada deuda
        total_pagado_calculado += d.total_pagado
        
        # Para el total adeudado, usamos una lógica más inteligente:
        if d.estado == 'Pagado':
            # Si una deuda está pagada, su "costo" fue lo que se pagó por ella.
            total_adeudado_calculado += d.total_pagado
        else:
            # Si no está pagada, su "costo" es su monto final actual (con recargos).
            total_adeudado_calculado += d.monto_final

    saldo_total_calculado = total_adeudado_calculado - total_pagado_calculado

    # --- LÓGICA ACADÉMICA ---
    inscripciones = InscripcionCurso.objects.filter(alumno=alumno).order_by('-curso__ciclo_lectivo')

    context = {
        'alumno': alumno,
        'deudas': deudas,
        'total_adeudado': total_adeudado_calculado,
        'total_pagado': total_pagado_calculado,
        'saldo_total': saldo_total_calculado,
        'inscripciones': inscripciones,
    }

    return render(request, 'alumnos/alumno/detail.html', context)
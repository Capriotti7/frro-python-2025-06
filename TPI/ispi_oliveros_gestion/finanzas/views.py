# finanzas/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.decorators import role_required
from .models import Deuda
from .forms import PagoForm, ConceptoPagoForm
from academico.models import Curso
from .models import ConceptoPago
from .services import generar_deudas_mensuales, generar_deudas_por_carrera
from django.db.models import Sum, Q
from alumnos.models import Alumno
from academico.models import Carrera

@login_required
@role_required('is_superuser', 'is_admin')
def registrar_pago_view(request, deuda_pk):
    deuda = get_object_or_404(Deuda, pk=deuda_pk)
    
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.deuda = deuda
            pago.save()
            messages.success(request, f'Se registró un pago de ${pago.monto_pagado} para la deuda de {deuda.concepto}.')
            return redirect('alumnos:alumno_detail', pk=deuda.alumno.pk)
    else:
        initial_data = {'monto_pagado': deuda.saldo}
        form = PagoForm(initial=initial_data)

    context = {
        'form': form,
        'deuda': deuda,
    }
    return render(request, 'finanzas/pago_form.html', context)

@login_required
@role_required('is_superuser', 'is_admin')
def gestion_financiera_view(request):
    conceptos = ConceptoPago.objects.all()
    carreras = Carrera.objects.all().order_by('nombre')
    
    # Estadísticas rápidas
    deudas_pendientes = Deuda.objects.filter(estado__in=['Pendiente', 'Vencido'])
    total_adeudado_real = sum(d.monto_final for d in deudas_pendientes)
    
    context = {
        'conceptos': conceptos,
        'carreras': carreras,
        'total_adeudado': total_adeudado_real,
        'cantidad_deudores': deudas_pendientes.values('alumno').distinct().count(),
    }
    return render(request, 'finanzas/gestion_financiera.html', context)

@login_required
@role_required('is_superuser', 'is_admin')
def generar_deudas_view(request):
    if request.method == 'POST':
        concepto_pk = request.POST.get('concepto')
        mes = request.POST.get('mes')
        anio = request.POST.get('anio')
        vencimiento = request.POST.get('vencimiento')

        creadas, omitidas = generar_deudas_mensuales(concepto_pk, mes, anio, vencimiento)

        messages.success(request, f'Proceso completado: {creadas} deudas nuevas generadas. {omitidas} alumnos ya tenían una deuda para este período y fueron omitidos.')
    
    return redirect('finanzas:gestion_financiera')

@login_required
@role_required('is_superuser', 'is_admin')
def generar_deudas_carrera_view(request):
    if request.method == 'POST':
        carrera_pk = request.POST.get('carrera')
        mes = int(request.POST.get('mes'))
        anio = int(request.POST.get('anio'))
        
        creadas, omitidas, error = generar_deudas_por_carrera(carrera_pk, mes, anio)
        
        if error:
            messages.error(request, f"Error|{error}")
        else:
            messages.success(request, f'Éxito|Proceso completado: {creadas} cuotas generadas. {omitidas} alumnos omitidos.')
    
    return redirect('finanzas:gestion_financiera')

# --- VISTAS PARA CONCEPTO DE PAGO ---
@login_required
@role_required('is_superuser', 'is_admin')
def concepto_pago_list_view(request):
    conceptos = ConceptoPago.objects.all().order_by('descripcion')
    return render(request, 'finanzas/concepto/list.html', {'conceptos': conceptos})

@login_required
@role_required('is_superuser', 'is_admin')
def concepto_pago_create_view(request):
    if request.method == 'POST':
        form = ConceptoPagoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Concepto de Pago Creado|El nuevo concepto ha sido guardado.')
            return redirect('finanzas:concepto_pago_list')
    else:
        form = ConceptoPagoForm()
    return render(request, 'finanzas/concepto/form.html', {'form': form})

@login_required
@role_required('is_superuser', 'is_admin')
def concepto_pago_update_view(request, pk):
    concepto = get_object_or_404(ConceptoPago, pk=pk)
    if request.method == 'POST':
        form = ConceptoPagoForm(request.POST, instance=concepto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Concepto de Pago Actualizado|Los cambios han sido guardados.')
            return redirect('finanzas:concepto_pago_list')
    else:
        form = ConceptoPagoForm(instance=concepto)
    return render(request, 'finanzas/concepto/form.html', {'form': form, 'concepto': concepto})

@login_required
@role_required('is_superuser', 'is_admin')
def concepto_pago_delete_view(request, pk): 
    concepto = get_object_or_404(ConceptoPago, pk=pk)
    if request.method == 'POST':
        concepto.delete()
        messages.success(request, 'Concepto de Pago Eliminado|El concepto ha sido eliminado exitosamente.')
        return redirect('finanzas:concepto_pago_list')
    return render(request, 'finanzas/concepto/confirm_delete.html', {'concepto': concepto})

@login_required
@role_required('is_superuser', 'is_admin')
def listado_deudores_view(request):
    # Obtenemos alumnos que tienen al menos una deuda Pendiente o Vencida
    alumnos_con_deuda = Alumno.objects.filter(
        Q(deudas__estado='Pendiente') | Q(deudas__estado='Vencido')
    ).distinct()

    # Calculamos el saldo de cada alumno
    alumnos_deudores = []
    for alumno in alumnos_con_deuda:
        deudas_alumno = alumno.deudas.filter(estado__in=['Pendiente', 'Vencido'])
        saldo_total = sum(d.saldo for d in deudas_alumno)
        if saldo_total > 0:
            alumnos_deudores.append({
                'alumno': alumno,
                'saldo_total': saldo_total,
                'cantidad_deudas': deudas_alumno.count()
            })
            
    # Ordenamos por quien más debe
    alumnos_deudores.sort(key=lambda x: x['saldo_total'], reverse=True)

    context = {'alumnos_deudores': alumnos_deudores}
    return render(request, 'finanzas/reporte_deudores.html', context)

@login_required
@role_required('is_superuser', 'is_admin')
def deuda_list_view(request):
    # Lógica para eliminar una deuda si se recibe un POST
    if request.method == 'POST' and 'delete_deuda_pk' in request.POST:
        deuda_a_eliminar = get_object_or_404(Deuda, pk=request.POST.get('delete_deuda_pk'))
        deuda_a_eliminar.delete()
        messages.success(request, 'Éxito|La deuda ha sido eliminada correctamente.')
        return redirect('finanzas:deuda_list')

    # Lógica para mostrar la lista
    deudas = Deuda.objects.all().select_related('alumno', 'concepto').order_by('-fecha_vencimiento')
    context = {'deudas': deudas}
    return render(request, 'finanzas/deuda/list.html', context)
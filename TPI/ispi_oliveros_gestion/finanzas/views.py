# finanzas/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Deuda
from .forms import PagoForm, ConceptoPagoForm
from academico.models import Curso # Necesitaremos esto más adelante
from .models import ConceptoPago # Y esto para el formulario
from .services import generar_deudas_mensuales

@login_required
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
def gestion_financiera_view(request):
    conceptos = ConceptoPago.objects.all()
    
    context = {
        'conceptos': conceptos
    }
    return render(request, 'finanzas/gestion_financiera.html', context)

@login_required
def generar_deudas_view(request):
    if request.method == 'POST':
        concepto_pk = request.POST.get('concepto')
        mes = request.POST.get('mes')
        anio = request.POST.get('anio')
        vencimiento = request.POST.get('vencimiento')

        creadas, omitidas = generar_deudas_mensuales(concepto_pk, mes, anio, vencimiento)

        messages.success(request, f'Proceso completado: {creadas} deudas nuevas generadas. {omitidas} alumnos ya tenían una deuda para este período y fueron omitidos.')
    
    return redirect('finanzas:gestion_financiera')

# --- VISTAS PARA CONCEPTO DE PAGO ---
@login_required
def concepto_pago_list_view(request):
    conceptos = ConceptoPago.objects.all().order_by('descripcion')
    return render(request, 'finanzas/concepto/list.html', {'conceptos': conceptos})

@login_required
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
def concepto_pago_delete_view(request, pk): 
    concepto = get_object_or_404(ConceptoPago, pk=pk)
    if request.method == 'POST':
        concepto.delete()
        messages.success(request, 'Concepto de Pago Eliminado|El concepto ha sido eliminado exitosamente.')
        return redirect('finanzas:concepto_pago_list')
    return render(request, 'finanzas/concepto/confirm_delete.html', {'concepto': concepto})
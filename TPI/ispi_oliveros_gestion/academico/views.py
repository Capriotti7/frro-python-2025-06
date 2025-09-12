# academico/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Carrera, Materia
from .forms import CarreraForm, MateriaForm


# --- VISTAS PARA CARRERA ---
@login_required
def carrera_list_view(request):
    carreras = Carrera.objects.all().order_by('nombre')
    context = {'carreras': carreras}
    return render(request, 'academico/carrera_list.html', context)

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
    return render(request, 'academico/carrera_form.html', context)

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
    return render(request, 'academico/carrera_form.html', context)

@login_required
def carrera_delete_view(request, pk):
    carrera = get_object_or_404(Carrera, pk=pk)
    if request.method == 'POST':
        carrera.delete()
        messages.success(request, 'La carrera ha sido eliminada.')
        return redirect('academico:carrera_list')
    context = {'carrera': carrera}
    return render(request, 'academico/carrera_confirm_delete.html', context)

# --- VISTAS PARA MATERIA ---
@login_required
def materia_list_view(request, carrera_pk):
    carrera = get_object_or_404(Carrera, pk=carrera_pk)
    materias = Materia.objects.filter(carrera=carrera).order_by('anio_carrera', 'nombre')
    context = {'carrera': carrera, 'materias': materias}
    return render(request, 'academico/materia_list.html', context)

@login_required
def materia_create_view(request, carrera_pk):
    carrera = get_object_or_404(Carrera, pk=carrera_pk)
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            # Usamos commit=False para detener el guardado
            materia = form.save(commit=False)
            # Asignamos la carrera manualmente
            materia.carrera = carrera
            # Ahora sí, guardamos el objeto completo
            materia.save()
            messages.success(request, 'La materia ha sido creada exitosamente.')
            return redirect('academico:materia_list', carrera_pk=carrera.pk)
    else:
        form = MateriaForm()
    context = {'form': form, 'carrera': carrera}
    return render(request, 'academico/materia_form.html', context)

@login_required
def materia_update_view(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    if request.method == 'POST':
        form = MateriaForm(request.POST, instance=materia)
        if form.is_valid():
            form.save()
            messages.success(request, 'La materia ha sido actualizada exitosamente.')
            return redirect('academico:materia_list', carrera_pk=materia.carrera.pk)
    else:
        form = MateriaForm(instance=materia)
    context = {'form': form, 'carrera': materia.carrera}
    return render(request, 'academico/materia_form.html', context)

@login_required
def materia_delete_view(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    if request.method == 'POST':
        carrera_pk = materia.carrera.pk
        materia.delete()
        messages.success(request, 'La materia ha sido eliminada.')
        return redirect('academico:materia_list', carrera_pk=carrera_pk)
    context = {'materia': materia}
    return render(request, 'academico/materia_confirm_delete.html', context)
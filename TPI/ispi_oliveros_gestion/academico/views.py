# academico/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Carrera, Materia, Curso
from .forms import CarreraForm, MateriaForm, CursoForm


# --- VISTAS PARA CARRERA ---
@login_required
def carrera_list_view(request):
    carreras = Carrera.objects.all().order_by('nombre')
    context = {'carreras': carreras}
    return render(request, 'academico/carrera/list.html', context)

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
    context = {'materia': materia, 'cursos': cursos}
    return render(request, 'academico/curso/list.html', context)

@login_required
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
def curso_delete_view(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        materia_pk = curso.materia.pk
        curso.delete()
        messages.success(request, 'El curso ha sido eliminado.')
        return redirect('academico:curso_list', materia_pk=materia_pk)
    context = {'curso': curso}
    return render(request, 'academico/curso/confirm_delete.html', context)
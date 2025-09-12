# alumnos/views.py

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Alumno 
from .forms import AlumnoForm

@login_required
def alumno_list_view(request):

    alumnos = Alumno.objects.all().order_by('apellido', 'nombre')

    context = {
        'alumnos': alumnos
    }
    return render(request, 'alumnos/alumno_list.html', context)

@login_required
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
    return render(request, 'alumnos/alumno_form.html', context)

@login_required
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
    return render(request, 'alumnos/alumno_form_edit.html', context)

@login_required
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
    return render(request, 'alumnos/alumno_confirm_delete.html', context)

@login_required
def alumno_detail_view(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)

    context = {
        'alumno': alumno,
    }
    return render(request, 'alumnos/alumno_detail.html', context)
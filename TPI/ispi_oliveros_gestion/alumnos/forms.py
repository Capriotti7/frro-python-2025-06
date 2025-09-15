# alumnos/forms.py

from django import forms
from .models import Alumno

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = [
            'dni',
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'email',
            'telefono',
            'direccion',
            'localidad',
            'nacionalidad',
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'AAAA-MM-DD'}
            ),
        }
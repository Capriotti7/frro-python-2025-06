# academico/forms.py

from django import forms
from .models import Carrera, Materia, Curso
from core.models import Docente
import datetime

class CarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = ['nombre', 'duracion_anios', 'tipo_titulacion', 'resolucion_ministerial']

class MateriaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        carrera = kwargs.pop('carrera', None)
        super(MateriaForm, self).__init__(*args, **kwargs)

        if carrera:
            year_choices = [
                (i, f'{i}° Año') for i in range(1, carrera.duracion_anios + 1)
            ]
            
            self.fields['anio_carrera'] = forms.ChoiceField(
                choices=year_choices,
                label="Año de la carrera",
            )

    class Meta:
        model = Materia
        fields = ['nombre', 'anio_carrera', 'modalidad_cursado']

def get_years():
    current_year = datetime.date.today().year
    return [(year, year) for year in range(current_year, current_year + 6)]

class CursoForm(forms.ModelForm):
    ciclo_lectivo = forms.ChoiceField(choices=get_years)

    class Meta:
        model = Curso
        fields = ['ciclo_lectivo', 'cuatrimestre', 'docente', 'dia_cursado', 'hora_inicio', 'hora_fin']
        # Añadimos widgets para los campos de hora
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = ['dni', 'nombre', 'apellido', 'email', 'telefono']
        widgets = {
            'dni': forms.TextInput(attrs={'placeholder': 'Ej: 12345678'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre completo'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Apellido(s)'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ej: 3415123456'}),
        }
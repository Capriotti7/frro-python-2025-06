# academico/forms.py

from django import forms
from .models import Carrera, Materia

class CarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = [
            'nombre', 
            'duracion_anios', 
            'tipo_titulacion', 
            'resolucion_ministerial']

class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia

        fields = [
            'nombre', 
            'anio_carrera']
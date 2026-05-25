# finanzas/forms.py

from django import forms
from .models import Pago, ConceptoPago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['monto_pagado', 'medio_de_pago', 'observaciones']

class ConceptoPagoForm(forms.ModelForm):
    class Meta:
        model = ConceptoPago
        fields = ['descripcion', 'tipo', 'monto_sugerido']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Removemos 'CUOTA_MENSUAL' de las opciones seleccionables porque se gestiona automático.
        if 'tipo' in self.fields:
            self.fields['tipo'].choices = [choice for choice in self.fields['tipo'].choices if choice[0] != 'CUOTA_MENSUAL']
            if not self.instance.pk:
                self.fields['tipo'].initial = 'OTRO'
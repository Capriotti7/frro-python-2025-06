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
        fields = ['descripcion', 'monto_sugerido']
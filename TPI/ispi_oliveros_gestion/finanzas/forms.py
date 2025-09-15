# finanzas/forms.py

from django import forms
from .models import Pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['monto_pagado', 'medio_de_pago', 'observaciones']
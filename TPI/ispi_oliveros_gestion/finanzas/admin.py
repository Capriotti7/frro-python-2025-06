# finanzas/admin.py

from django.contrib import admin
from .models import ConceptoPago, Deuda, Pago

admin.site.register(ConceptoPago)
admin.site.register(Deuda)
admin.site.register(Pago)
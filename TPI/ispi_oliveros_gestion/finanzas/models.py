from django.db import models
from alumnos.models import Alumno


class ConceptoPago(models.Model):
    descripcion = models.CharField(max_length=150)  # Ej: "Matrícula 2025", "Cuota Mensual"
    monto_sugerido = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.descripcion


class Deuda(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="deudas")
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    mes_correspondiente = models.IntegerField()
    anio_correspondiente = models.IntegerField()
    estado = models.CharField(max_length=20, choices=[
        ("Pendiente", "Pendiente"),
        ("Pagada", "Pagada"),
        ("Vencida", "Vencida"),
    ])

    def __str__(self):
        return f"Deuda {self.mes_correspondiente}/{self.anio_correspondiente} - {self.alumno}"


class Pago(models.Model):
    deuda = models.ForeignKey(Deuda, on_delete=models.CASCADE, related_name="pagos")
    concepto = models.ForeignKey(ConceptoPago, on_delete=models.CASCADE, related_name="pagos")
    fecha_pago = models.DateField(auto_now_add=True)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    medio_de_pago = models.CharField(max_length=50, choices=[
        ("Efectivo", "Efectivo"),
        ("Transferencia", "Transferencia"),
        ("Tarjeta", "Tarjeta"),
    ])
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pago {self.monto_pagado} - {self.alumno}"
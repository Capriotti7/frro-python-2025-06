from django.db import models
from alumnos.models import Alumno
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal


class ConceptoPago(models.Model):
    descripcion = models.CharField(max_length=200)
    monto_sugerido = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.descripcion


class Deuda(models.Model):
    ESTADOS = [
        ("Pendiente", "Pendiente"),
        ("Pagado", "Pagado"),
        ("Vencido", "Vencido"),
    ]
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="deudas")
    concepto = models.ForeignKey(ConceptoPago, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    mes_correspondiente = models.IntegerField(blank=True, null=True)
    anio_correspondiente = models.IntegerField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="Pendiente")

    # --- MÉTODOS INTELIGENTES ---
    @property
    def total_pagado(self):
        # Suma todos los 'monto_pagado' de los pagos asociados a esta deuda.
        # El 'or 0' es para que devuelva 0 si no hay pagos, en lugar de None.
        return self.pagos.aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or 0

    @property
    def esta_vencida(self):
        return self.fecha_vencimiento < timezone.now().date()
    
    @property
    def recargo(self):
        # La condición principal: si no está vencida, no hay recargo.
        if self.estado != 'Vencido':
            return 0
        
        # Segunda condición: si ya está pagada (aunque el estado sea 'Vencido' por error), no hay recargo.
        if self.total_pagado >= self.monto:
            return 0
        
        # Si llegamos aquí, la deuda está Vencida y tiene un saldo pendiente sobre el monto original.
        hoy = timezone.now().date()

        # Lógica para cuotas mensuales
        if self.concepto.descripcion.lower() == 'cuota mensual':
            # Verificamos si estamos en el mismo mes del vencimiento
            if hoy.year == self.fecha_vencimiento.year and hoy.month == self.fecha_vencimiento.month:
                # Recargo del 5% dentro del mes de vencimiento
                return (self.monto * Decimal('0.05')).quantize(Decimal('0.01'))
            else:
                # Recargo del 10% para meses posteriores (a mes vencido)
                return (self.monto * Decimal('0.10')).quantize(Decimal('0.01'))
        
        # Lógica para otras deudas vencidas (ej. 10% fijo)
        else:
            return (self.monto * Decimal('0.10')).quantize(Decimal('0.01'))
    
    @property
    def monto_final(self):
        return self.monto + self.recargo

    @property
    def saldo(self):
        # Calcula el saldo restando lo pagado del monto total.
        return self.monto_final - self.total_pagado  

    def __str__(self):
        return f"Deuda de {self.alumno} por {self.concepto} - ${self.monto}"


class Pago(models.Model):
    deuda = models.ForeignKey(Deuda, on_delete=models.CASCADE, related_name="pagos")
    fecha_pago = models.DateField(auto_now_add=True)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    medio_de_pago = models.CharField(max_length=50, default="Efectivo")
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pago de ${self.monto_pagado} para la deuda de {self.deuda.concepto}"
    
    # --- MÉTODO SAVE MEJORADO ---
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        deuda_asociada = self.deuda
        if deuda_asociada.saldo <= 0:
            deuda_asociada.estado = "Pagado"
        else:
            if deuda_asociada.estado == "Vencido":
                deuda_asociada.estado = "Pendiente"
        
        deuda_asociada.save()
# finanzas/services.py

from alumnos.models import Alumno
from .models import ConceptoPago, Deuda
from datetime import date

def generar_deudas_mensuales(concepto_pk, mes, anio, fecha_vencimiento):
    
    """ Genera deudas para todos los alumnos que no tengan ya una deuda
    para el mismo concepto, mes y año. """

    concepto = ConceptoPago.objects.get(pk=concepto_pk)
    alumnos_activos = Alumno.objects.all() # En el futuro, podríamos filtrar por 'alumno.activo=True'
    
    deudas_creadas = 0
    alumnos_omitidos = 0

    for alumno in alumnos_activos:
        # Verificamos si ya existe una deuda para este alumno, concepto, mes y año
        deuda_existente = Deuda.objects.filter(
            alumno=alumno,
            concepto=concepto,
            mes_correspondiente=mes,
            anio_correspondiente=anio
        ).exists()

        if not deuda_existente:
            Deuda.objects.create(
                alumno=alumno,
                concepto=concepto,
                monto=concepto.monto_sugerido,
                fecha_vencimiento=fecha_vencimiento,
                mes_correspondiente=mes,
                anio_correspondiente=anio,
                estado="Pendiente"
            )
            deudas_creadas += 1
        else:
            alumnos_omitidos += 1
            
    return deudas_creadas, alumnos_omitidos
# finanzas/services.py

from django.shortcuts import get_object_or_404
from alumnos.models import Alumno
from .models import ConceptoPago, Deuda
from datetime import date
from academico.models import Carrera, InscripcionCurso

def generar_deudas_mensuales(concepto_pk, mes, anio, fecha_vencimiento):     #ver si es necesario que siga existiendo
    
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

def generar_deudas_por_carrera(carrera_pk, mes, anio):
    """
    Genera la deuda de la cuota mensual para todos los alumnos inscriptos
    en un curso activo de una carrera específica para un período dado.
    """
    carrera = get_object_or_404(Carrera, pk=carrera_pk)
    
    # Buscamos el concepto de pago "Cuota Mensual". ¡Debe existir!
    # Creamos un try-except por si no existe, para evitar que la app crashee.
    try:
        concepto_cuota = ConceptoPago.objects.get(descripcion__iexact="Cuota Mensual")
    except ConceptoPago.DoesNotExist:
        return 0, 0, "Error: No se encontró el Concepto de Pago 'Cuota Mensual'."

    # Obtenemos el monto actual de la cuota para esta carrera.
    monto_cuota_actual = carrera.valor_cuota_actual
    if not monto_cuota_actual or monto_cuota_actual <= 0:
        return 0, 0, f"Error: La carrera '{carrera.nombre}' no tiene un valor de cuota vigente configurado."

    # Encontrar alumnos de la carrera: Buscamos alumnos inscriptos a cursos de esta carrera en este ciclo lectivo
    alumnos_de_la_carrera = Alumno.objects.filter(
        inscripciones__curso__materia__carrera=carrera,
        inscripciones__curso__ciclo_lectivo=anio
    ).distinct()

    # La fecha de vencimiento es siempre el 15 del mes.
    fecha_vencimiento = date(anio, mes, 15)
    
    deudas_creadas = 0
    alumnos_omitidos = 0

    for alumno in alumnos_de_la_carrera:
        deuda_existente = Deuda.objects.filter(
            alumno=alumno,
            concepto=concepto_cuota,
            mes_correspondiente=mes,
            anio_correspondiente=anio
        ).exists()

        if not deuda_existente:
            Deuda.objects.create(
                alumno=alumno,
                concepto=concepto_cuota,
                monto=monto_cuota_actual,
                fecha_vencimiento=fecha_vencimiento,
                mes_correspondiente=mes,
                anio_correspondiente=anio,
                estado="Pendiente"
            )
            deudas_creadas += 1
        else:
            alumnos_omitidos += 1
            
    return deudas_creadas, alumnos_omitidos, None
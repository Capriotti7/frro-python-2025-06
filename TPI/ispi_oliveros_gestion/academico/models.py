from django.db import models
from alumnos.models import Alumno


class Docente(models.Model):
    dni = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"


class Carrera(models.Model):
    TIPOS_TITULACION = [
        ("Tecnicatura", "Tecnicatura"),
        ("Licenciatura", "Licenciatura"),
        ("Curso", "Curso"),
    ]

    nombre = models.CharField(max_length=150)
    duracion_anios = models.IntegerField()
    tipo_titulacion = models.CharField(max_length=20, choices=TIPOS_TITULACION)
    resolucion_ministerial = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Materia(models.Model):
    nombre = models.CharField(max_length=150)
    anio_carrera = models.IntegerField()  # ej: 1, 2, 3
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name="materias")

    def __str__(self):
        return f"{self.nombre} ({self.carrera.nombre})"


class Curso(models.Model):
    ciclo_lectivo = models.IntegerField()
    cuatrimestre = models.IntegerField()
    horarios = models.CharField(max_length=200)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, related_name="cursos")
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="cursos")

    def __str__(self):
        return f"{self.materia.nombre} - {self.ciclo_lectivo}/{self.cuatrimestre}"


class InscripcionCurso(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="inscripciones")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="inscripciones")
    fecha_inscripcion = models.DateField(auto_now_add=True)
    nota_final = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    condicion = models.CharField(max_length=50, choices=[
        ("Regular", "Regular"),
        ("Libre", "Libre"),
        ("Promocionado", "Promocionado"),
    ], blank=True, null=True)

    def __str__(self):
        return f"{self.alumno} - {self.curso}"


class Asistencia(models.Model):
    inscripcion = models.ForeignKey(InscripcionCurso, on_delete=models.CASCADE, related_name="asistencias")
    fecha_clase = models.DateField()
    estado = models.CharField(max_length=20, choices=[
        ("Presente", "Presente"),
        ("Ausente", "Ausente"),
        ("Justificado", "Justificado"),
    ])

    def __str__(self):
        return f"{self.inscripcion.alumno} - {self.fecha_clase}: {self.estado}"

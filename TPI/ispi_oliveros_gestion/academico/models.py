from django.db import models
from alumnos.models import Alumno
from django.contrib.auth.models import User


class Docente(models.Model):
 
    # Añadimos null=True y blank=True
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_docente', null=True, blank=True)

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

    YEAR_CHOICES = [
        (1, "1 Año"),
        (2, "2 Años"),
        (3, "3 Años"),
        (4, "4 Años"),
        (5, "5 Años"),
    ]

    nombre = models.CharField(max_length=150)
    duracion_anios = models.IntegerField(choices=YEAR_CHOICES, default=3)
    tipo_titulacion = models.CharField(max_length=20, choices=TIPOS_TITULACION)
    resolucion_ministerial = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Materia(models.Model):
    MODALIDADES = [
        ("Anual", "Anual"),
        ("1C", "1er Cuatrimestre"),
        ("2C", "2do Cuatrimestre"),
    ]

    nombre = models.CharField(max_length=150)
    anio_carrera = models.IntegerField()
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name="materias")
    modalidad_cursado = models.CharField(max_length=5, choices=MODALIDADES, default="1C")

    def __str__(self):
        return f"{self.nombre} ({self.carrera.nombre})"


class Curso(models.Model):
    DIAS_SEMANA = [
        (1, "Lunes"),
        (2, "Martes"),
        (3, "Miércoles"),
        (4, "Jueves"),
        (5, "Viernes"),
        (6, "Sábado"),
    ]
    
    CUATRIMESTRES = [
        (0, "Anual"),
        (1, "1er Cuatrimestre"),
        (2, "2do Cuatrimestre"),
    ]

    ciclo_lectivo = models.IntegerField()
    cuatrimestre = models.IntegerField(choices=CUATRIMESTRES, default=1)
    docente = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True, blank=True, related_name="cursos")
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="cursos")

    dia_cursado = models.IntegerField(choices=DIAS_SEMANA, default=1)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.materia.nombre} - {self.ciclo_lectivo}/{self.get_cuatrimestre_display()}"


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


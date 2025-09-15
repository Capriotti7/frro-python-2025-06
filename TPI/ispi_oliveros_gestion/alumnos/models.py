from django.db import models


class Alumno(models.Model):
    dni = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    localidad = models.CharField(max_length=100, blank=True, null=True)
    nacionalidad = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"


class DocumentacionAlumno(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="documentacion")
    nombre = models.CharField(max_length=100)
    fecha_entrega = models.DateField()
    estado = models.CharField(max_length=50, choices=[("Aprobado", "Aprobado"), ("Pendiente", "Pendiente")])
    archivo_adjunto = models.FileField(upload_to="documentacion/")

    def __str__(self):
        return f"{self.nombre} - {self.alumno}"

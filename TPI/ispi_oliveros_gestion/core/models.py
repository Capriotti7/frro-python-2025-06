from django.db import models
from django.contrib.auth.models import User

# Creamos un nuevo modelo para el perfil de Administrador
class Administrador(models.Model):
    # Enlazamos este perfil a una única cuenta de usuario.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_administrador')

    def __str__(self):
        # Para que se muestre bien en el panel de administración
        return f"Perfil Admin de: {self.user.username}"

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
    

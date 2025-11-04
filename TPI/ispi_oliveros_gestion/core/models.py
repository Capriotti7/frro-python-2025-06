from django.db import models
from django.contrib.auth.models import User

# Creamos un nuevo modelo para el perfil de Administrador
class Administrador(models.Model):
    # Enlazamos este perfil a una única cuenta de usuario.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_administrador')

    def __str__(self):
        # Para que se muestre bien en el panel de administración
        if self.user.last_name and self.user.first_name:
            # Opción 1: Si tenemos ambos datos
            return f"{self.user.last_name}, {self.user.first_name}"
        elif self.user.last_name:
            # Opción 2: Si solo tenemos apellido
            return self.user.last_name
        else:
            # Opción 3: Como último recurso, el username
            return self.user.username

class Docente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_docente')
    dni = models.CharField(max_length=20, unique=True, verbose_name="DNI")
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        # Para que se muestre bien en el panel de docente
        if self.user.last_name and self.user.first_name:
            # Opción 1: Si tenemos ambos datos
            return f"{self.user.last_name}, {self.user.first_name}"
        elif self.user.last_name:
            # Opción 2: Si solo tenemos apellido
            return self.user.last_name
        else:
            # Opción 3: Como último recurso, el username
            return self.user.username


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

class SolicitudRegistro(models.Model):
    PERFILES = (
        ('ADMIN', 'Administrativo'),
        ('DOCENTE', 'Docente'),
    )
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    )

    # Datos para el User de Django
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    # Guardamos el hash de la contraseña, no el texto plano
    password_hash = models.CharField(max_length=128) 

    # Datos específicos del rol
    dni = models.CharField(max_length=20, blank=True, null=True, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    
    # Datos de la solicitud
    tipo_perfil = models.CharField(max_length=10, choices=PERFILES)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='PENDIENTE')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitud de {self.username} como {self.get_tipo_perfil_display()}"
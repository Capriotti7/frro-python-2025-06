from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from academico.models import Docente
from core.models import Administrador

class RegistroConCodigoForm(forms.Form):
    # Campos del User de Django
    username = forms.CharField(max_length=150, required=True, label="Nombre de Usuario")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Contraseña")
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True, label="Nombre")
    last_name = forms.CharField(max_length=150, required=True, label="Apellido")
    
    # Campo para el código secreto
    codigo_registro = forms.CharField(max_length=50, required=True, label="Código de Registro")

    # Campos específicos para el perfil de Docente (solo se usarán si el código es de docente)
    dni = forms.CharField(max_length=20, required=False)
    telefono = forms.CharField(max_length=20, required=False)

    def clean_codigo_registro(self):
        """ Valida que el código de registro sea uno de los permitidos. """
        codigo = self.cleaned_data.get('codigo_registro')
        if codigo not in [settings.CODIGO_REGISTRO_ADMIN, settings.CODIGO_REGISTRO_DOCENTE]:
            raise forms.ValidationError("El código de registro no es válido.")
        return codigo

    def clean(self):
        """ Valida que los campos de docente sean obligatorios si el código es de docente. """
        cleaned_data = super().clean()
        codigo = cleaned_data.get('codigo_registro')

        if codigo == settings.CODIGO_REGISTRO_DOCENTE:
            if not cleaned_data.get('dni'):
                self.add_error('dni', 'El DNI es obligatorio para registrar un docente.')
            if not cleaned_data.get('telefono'):
                self.add_error('telefono', 'El teléfono es obligatorio para registrar un docente.')
        return cleaned_data

    def save(self):
        """ Crea el User y el perfil correspondiente según el código. """
        data = self.cleaned_data
        
        # 1. Crear el objeto User
        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        
        # 2. Crear el perfil según el código
        codigo = data['codigo_registro']
        if codigo == settings.CODIGO_REGISTRO_ADMIN:
            Administrador.objects.create(user=user)
        
        elif codigo == settings.CODIGO_REGISTRO_DOCENTE:
            Docente.objects.create(
                user=user,
                dni=data['dni'],
                nombre=data['first_name'],
                apellido=data['last_name'],
                email=data['email'],
                telefono=data['telefono']
            )
            
        return user
    
    def clean_username(self):
        """ Valida que el nombre de usuario no esté ya en uso. """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso. Por favor, elige otro.")
        return username

    def clean_email(self):
        """ Valida que el correo electrónico no esté ya en uso. """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Esta dirección de correo electrónico ya está registrada.")
        return email

    def clean_dni(self):
        """ Valida que el DNI no esté ya en uso por otro docente. """
        dni = self.cleaned_data.get('dni')
        # Solo validamos el DNI si se está intentando registrar un docente
        if self.cleaned_data.get('codigo_registro') == settings.CODIGO_REGISTRO_DOCENTE:
            if Docente.objects.filter(dni=dni).exists():
                raise forms.ValidationError("Este DNI ya está registrado a nombre de otro docente.")
        return dni
# academico/forms.py

from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Carrera, Materia, Curso, ValorCarrera
from core.models import Docente
import datetime

class CarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = ['nombre', 'duracion_anios', 'tipo_titulacion', 'resolucion_ministerial']

    def clean(self):
        """
        Este método se usa para validaciones que involucran
        múltiples campos del formulario a la vez.
        """
        cleaned_data = super().clean()

        # 2. Prepara la consulta para buscar duplicados
        query = Carrera.objects.filter(
            nombre=cleaned_data.get('nombre'),
            duracion_anios=cleaned_data.get('duracion_anios'),
            tipo_titulacion=cleaned_data.get('tipo_titulacion'),
            resolucion_ministerial=cleaned_data.get('resolucion_ministerial')
        )

        # Si 'self.instance.pk' existe, significa que estamos EDITANDO
        # una carrera existente. Debemos excluir a ESA MISMA carrera
        # de la búsqueda de duplicados.
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)

        # 4. Si la consulta encuentra algún resultado (query.exists()),
        # significa que ya existe otra carrera igual.
        if query.exists():
            raise forms.ValidationError(
                "¡Error! Ya existe una carrera con exactamente los mismos datos."
            )

        return cleaned_data

class ValorCarreraForm(forms.ModelForm):
    """
    Formulario para crear un nuevo registro en el historial de valores de una carrera.
    """
    class Meta:
        model = ValorCarrera
        # No incluimos 'carrera' porque la asignaremos automáticamente en la vista.
        fields = ['valor_cuota', 'fecha_vigencia']
        widgets = {
            'fecha_vigencia': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d' # Asegura que el formato sea compatible
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacemos los campos obligatorios por defecto un poco más amigables
        self.fields['valor_cuota'].label = "Nuevo Valor de Cuota"
        self.fields['fecha_vigencia'].label = "Vigente a partir de la Fecha"

    def clean_fecha_vigencia(self):
        """
        Valida que la fecha de vigencia no sea una fecha pasada.
        """
        fecha = self.cleaned_data.get('fecha_vigencia')
        
        hoy = timezone.now().date()

        # 3. Comparamos. Si la fecha es anterior a hoy, lanzamos un error.
        if fecha and fecha < hoy:
            raise forms.ValidationError("La fecha de vigencia no puede ser anterior al día de hoy.")
        
        return fecha

class MateriaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        carrera = kwargs.pop('carrera', None)
        super(MateriaForm, self).__init__(*args, **kwargs)

        if carrera:
            year_choices = [
                (i, f'{i}° Año') for i in range(1, carrera.duracion_anios + 1)
            ]
            
            self.fields['anio_carrera'] = forms.ChoiceField(
                choices=year_choices,
                label="Año de la carrera",
            )

    class Meta:
        model = Materia
        fields = ['nombre', 'anio_carrera', 'modalidad_cursado']

def get_years():
    current_year = datetime.date.today().year
    return [(year, year) for year in range(current_year, current_year + 6)]

class CursoForm(forms.ModelForm):
    ciclo_lectivo = forms.ChoiceField(choices=get_years)

    class Meta:
        model = Curso
        fields = ['ciclo_lectivo', 'cuatrimestre', 'docente', 'dia_cursado', 'hora_inicio', 'hora_fin']
        # Añadimos widgets para los campos de hora
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }

class DocenteForm(forms.Form):
    """
    Formulario para que un ADMINISTRADOR cree y actualice perfiles de Docentes.
    Maneja la lógica para los modelos User y Docente de forma centralizada.
    """
    first_name = forms.CharField(
        label="Nombre", 
        max_length=150, 
        widget=forms.TextInput(attrs={'placeholder': 'Nombre del docente'})
    )
    last_name = forms.CharField(
        label="Apellido", 
        max_length=150, 
        widget=forms.TextInput(attrs={'placeholder': 'Apellido del docente'})
    )
    username = forms.CharField(
        label="Nombre de Usuario", 
        max_length=150, 
        help_text="Se usará para iniciar sesión. Sin espacios ni caracteres especiales."
    )
    email = forms.EmailField(
        label="Email", 
        widget=forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'})
    )
    
    """ Campos específicos del perfil Docente """

    dni = forms.CharField(
        label="DNI", 
        max_length=20, 
        widget=forms.TextInput(attrs={'placeholder': 'Sin puntos ni espacios'})
    )
    telefono = forms.CharField(
        label="Teléfono", 
        max_length=20, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Opcional'})
    )
    
    # === CAMPO DE CONTRASEÑA (MANEJADO POR LA LÓGICA DEL FORMULARIO) ===
    password = forms.CharField(
        label="Contraseña", 
        widget=forms.PasswordInput, 
        required=False, 
        help_text="Dejar en blanco para no cambiarla al editar."
    )

    def __init__(self, *args, **kwargs):

        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        if self.instance:
            # MODO EDICIÓN: Rellenamos el formulario con los datos existentes.
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['dni'].initial = self.instance.dni
            self.fields['telefono'].initial = self.instance.telefono

            # El username no se debe poder cambiar una vez creado.
            self.fields['username'].disabled = True
            
            # La contraseña no es obligatoria al editar.
            self.fields['password'].required = False
        else:
            # MODO CREACIÓN: La contraseña sí es obligatoria.
            self.fields['password'].required = True

    def clean_username(self):
        # Validación para asegurar que el username sea único.
        username = self.cleaned_data['username']
        # Si estamos editando y el username no ha cambiado, es válido.
        if self.instance and self.instance.user.username == username:
            return username
        # Si el username ya existe en la base de datos, lanzamos un error.
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso. Por favor, elige otro.")
        return username

    def clean_email(self):
        # Validación para asegurar que el email sea único.
        email = self.cleaned_data['email']
        if self.instance and self.instance.user.email == email:
            return email
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Esta dirección de email ya está registrada.")
        return email

    def save(self):
        # Este es el método principal que guarda los datos en la base de datos.
        if self.instance:
            user = self.instance.user
            docente = self.instance
            
            # 1. Actualizar datos del User
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            
            # 2. Actualizar contraseña SOLO si se escribió una nueva
            password = self.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()

            # 3. Actualizar datos del perfil Docente
            docente.dni = self.cleaned_data['dni']
            docente.telefono = self.cleaned_data['telefono']
            docente.save()

        else:
            # 1. Crear el objeto User
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )

            # 2. Crear el objeto Docente y enlazarlo al User recién creado
            docente = Docente.objects.create(
                user=user,
                dni=self.cleaned_data['dni'],
                telefono=self.cleaned_data['telefono']
            )
        
        return docente
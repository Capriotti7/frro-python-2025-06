from django import forms
from django.contrib.auth.models import User
from .models import Administrador

class AdministradorForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Nombre de usuario")
    first_name = forms.CharField(max_length=150, required=True, label="Nombre")
    last_name = forms.CharField(max_length=150, required=True, label="Apellido")
    email = forms.EmailField(required=True, label="Correo electrónico")
    password = forms.CharField(
        widget=forms.PasswordInput, 
        required=False, 
        label="Contraseña",
        help_text="Déjelo en blanco si no desea cambiar la contraseña al editar."
    )

    class Meta:
        model = Administrador
        fields = [] # Campos específicos del perfil se agregan aquí si el modelo crece.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estamos editando, cargar los datos actuales del User
        if self.instance and self.instance.pk:
            self.fields['username'].initial = self.instance.user.username
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
        else:
            self.fields['password'].required = True

    def clean_username(self):
        username = self.cleaned_data['username']
        query = User.objects.filter(username=username)
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.user.pk)
        if query.exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso.')
        return username

    def save(self, commit=True):
        admin_instance = super().save(commit=False)
        username = self.cleaned_data['username']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        # Crear o actualizar el user
        if self.instance.pk:
            user = self.instance.user
        else:
            user = User()

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
            admin_instance.user = user
            admin_instance.save()
        
        return admin_instance

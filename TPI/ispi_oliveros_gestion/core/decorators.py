from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def group_required(*group_names):
    """
    Decorador que restringe el acceso a usuarios que pertenecen
    a al menos uno de los grupos especificados.
    """
    def in_groups(user):
        if user.is_authenticated:
            if bool(user.groups.filter(name__in=group_names)) or user.is_superuser:
                return True
        raise PermissionDenied
    
    return user_passes_test(in_groups)

def superuser_required(function):
    """
    Decorador que verifica que el usuario logueado sea un superusuario.
    Si no lo es, levanta una excepción de Permiso Denegado.
    """
    def wrap(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return wrap

def role_required(*roles):
    """
    Decorador que verifica que el usuario logueado tenga al menos uno de los roles especificados.
    Roles pueden ser: 'is_superuser', 'is_admin', 'is_docente'.
    """
    def decorator(function):
        def wrap(request, *args, **kwargs):
            user = request.user
            
            # --- SE USA hasattr() AQUÍ PORQUE ESTAMOS EN CÓDIGO PYTHON ---
            user_roles = {
                'is_superuser': user.is_superuser,
                'is_admin': hasattr(user, 'perfil_administrador'),
                'is_docente': hasattr(user, 'perfil_docente'),
            }
            
            if any(user_roles.get(role) for role in roles):
                return function(request, *args, **kwargs)
            
            raise PermissionDenied
        return wrap
    return decorator
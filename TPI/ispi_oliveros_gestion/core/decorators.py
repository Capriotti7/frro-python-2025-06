from django.core.exceptions import PermissionDenied

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
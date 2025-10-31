from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

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
# academico/admin.py

from django.contrib import admin
from .models import Carrera, Materia, Curso
from core.models import Docente

class DocenteAdmin(admin.ModelAdmin):

    list_display = ('user__last_name', 'user__first_name', 'dni', 'user__email')

    search_fields = ('user__last_name', 'user__first_name', 'dni', 'user__email')

admin.site.register(Docente, DocenteAdmin)
# admin.site.register(Carrera)
# admin.site.register(Materia)        VER SI ESTOS SON NECESARIOS, CREO QUE SON REDUNDANTES
# admin.site.register(Curso)
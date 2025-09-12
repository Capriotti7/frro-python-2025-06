# academico/admin.py

from django.contrib import admin
from .models import Docente, Carrera, Materia, Curso


class DocenteAdmin(admin.ModelAdmin):

    list_display = ('apellido', 'nombre', 'dni', 'email')

    search_fields = ('apellido', 'nombre', 'dni')

admin.site.register(Docente, DocenteAdmin)
admin.site.register(Carrera)
admin.site.register(Materia)
admin.site.register(Curso)
# academico/urls.py

from django.urls import path
from . import views

app_name = 'academico'

urlpatterns = [
    # URLs de Carreras
    path('carreras/', views.carrera_list_view, name='carrera_list'),
    path('carreras/agregar/', views.carrera_create_view, name='carrera_add'),
    path('carreras/<int:pk>/editar/', views.carrera_update_view, name='carrera_edit'),
    path('carreras/<int:pk>/eliminar/', views.carrera_delete_view, name='carrera_delete'),

    # URLs de Materias (anidadas bajo una carrera)
    path('carreras/<int:carrera_pk>/materias/', views.materia_list_view, name='materia_list'),
    path('carreras/<int:carrera_pk>/materias/agregar/', views.materia_create_view, name='materia_add'),
    path('materias/<int:pk>/editar/', views.materia_update_view, name='materia_edit'),
    path('materias/<int:pk>/eliminar/', views.materia_delete_view, name='materia_delete'),

    # URLs de Cursos (anidadas bajo una materia)
    path('materias/<int:materia_pk>/cursos/', views.curso_list_view, name='curso_list'),
    path('materias/<int:materia_pk>/cursos/agregar/', views.curso_create_view, name='curso_add'),
    path('cursos/<int:pk>/editar/', views.curso_update_view, name='curso_edit'),
    path('cursos/<int:pk>/eliminar/', views.curso_delete_view, name='curso_delete'),

    path('docentes/', views.docente_list_view, name='docente_list'),
    path('docentes/agregar/', views.docente_create_view, name='docente_add'),
    path('docentes/<int:pk>/editar/', views.docente_update_view, name='docente_edit'),
    path('docentes/<int:pk>/eliminar/', views.docente_delete_view, name='docente_delete'),
    path('materias/<int:materia_pk>/docentes/', views.docente_list_from_materia_view, name='docente_list_from_materia'),
    path('materias/<int:materia_pk>/docentes/<int:pk>/eliminar/', views.docente_delete_from_materia_view, name='docente_delete_from_materia'),

    # URL para la página de selección de cursos para un alumno
    path('alumnos/<int:alumno_pk>/inscribir-a-curso/', views.curso_selection_list_view, name='curso_selection_list'),
    
    # URL para procesar la inscripción
    path('inscribir-ejecutar/', views.inscribir_alumno_ejecutar_view, name='inscribir_ejecutar'),

    # URL para la página de gestión de asistencias
    path('cursos/<int:curso_pk>/asistencias/', views.gestionar_asistencias_view, name='gestionar_asistencias'),

    # URL para ver el historial de asistencias de una inscripción
    path('inscripciones/<int:inscripcion_pk>/asistencias/', views.ver_asistencias_view, name='ver_asistencias'),

    # URL para la página de selección de cursos para asistencia
    path('asistencias/seleccionar-curso/', views.asistencia_seleccion_curso_view, name='asistencia_seleccion_curso'),
    # Para ver el detalle de un curso y su lista de inscriptos
    path('cursos/<int:curso_pk>/', views.curso_detail_view, name='curso_detail'),
    # Para ir a la página de búsqueda y selección de alumnos a inscribir
    path('cursos/<int:curso_pk>/inscribir/', views.curso_inscribir_alumno_list_view, name='curso_inscribir_alumno_list'),
    # La acción que inscribe a un alumno (se llamará con un POST)
    path('cursos/<int:curso_pk>/inscribir-accion/<int:alumno_pk>/', views.curso_inscribir_alumno_action_view, name='curso_inscribir_alumno_action'),
]
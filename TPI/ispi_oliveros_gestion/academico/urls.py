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
]
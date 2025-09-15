# alumnos/urls.py

from django.urls import path
from . import views

app_name = 'alumnos'

urlpatterns = [
    path('', views.alumno_list_view, name='alumno_list'),
    path('<int:pk>/', views.alumno_detail_view, name='alumno_detail'),
    path('agregar/', views.alumno_create_view, name='alumno_add'),
    path('<int:pk>/editar/', views.alumno_update_view, name='alumno_edit'),
    path('<int:pk>/eliminar/', views.alumno_delete_view, name='alumno_delete'),
]
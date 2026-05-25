# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # URLs para la gestión de solicitudes
    path('solicitudes/', views.gestion_solicitudes_view, name='gestion_solicitudes'),
    path('solicitudes/<int:solicitud_pk>/aprobar/', views.aprobar_solicitud_view, name='aprobar_solicitud'),
    path('solicitudes/<int:solicitud_pk>/rechazar/', views.rechazar_solicitud_view, name='rechazar_solicitud'),

    # Rutas para el CRUD de Administradores
    path('administradores/', views.AdministradorListView.as_view(), name='administrador_list'),
    path('administradores/nuevo/', views.AdministradorCreateView.as_view(), name='administrador_create'),
    path('administradores/<int:pk>/editar/', views.AdministradorUpdateView.as_view(), name='administrador_update'),
    path('administradores/<int:pk>/eliminar/', views.AdministradorDeleteView.as_view(), name='administrador_delete'),
]
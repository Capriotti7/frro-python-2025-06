# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # URLs para la gestión de solicitudes
    path('solicitudes/', views.gestion_solicitudes_view, name='gestion_solicitudes'),
    path('solicitudes/<int:solicitud_pk>/aprobar/', views.aprobar_solicitud_view, name='aprobar_solicitud'),
    path('solicitudes/<int:solicitud_pk>/rechazar/', views.rechazar_solicitud_view, name='rechazar_solicitud'),
]
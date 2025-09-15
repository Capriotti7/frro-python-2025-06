# finanzas/urls.py

from django.urls import path
from . import views

app_name = 'finanzas'

urlpatterns = [
    path('', views.gestion_financiera_view, name='gestion_financiera'),
    path('deudas/<int:deuda_pk>/registrar-pago/', views.registrar_pago_view, name='registrar_pago'),
    path('generar-deudas/', views.generar_deudas_view, name='generar_deudas'),
]
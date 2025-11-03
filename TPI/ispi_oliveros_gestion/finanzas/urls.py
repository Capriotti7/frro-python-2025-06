# finanzas/urls.py

from django.urls import path
from . import views

app_name = 'finanzas'

urlpatterns = [
    path('', views.gestion_financiera_view, name='gestion_financiera'),
    path('generar-deudas/', views.generar_deudas_view, name='generar_deudas'),

    # URLs para el ABM de Conceptos de Pago
    path('conceptos/', views.concepto_pago_list_view, name='concepto_pago_list'),
    path('conceptos/agregar/', views.concepto_pago_create_view, name='concepto_pago_add'),
    path('conceptos/<int:pk>/editar/', views.concepto_pago_update_view, name='concepto_pago_edit'),
    path('conceptos/<int:pk>/eliminar/', views.concepto_pago_delete_view, name='concepto_pago_delete'),
    
    # URLs para la gestión de Deudas y Pagos
    path('deudas/<int:deuda_pk>/registrar-pago/', views.registrar_pago_view, name='registrar_pago'),
]
from django.urls import path

from .views import VentasView,VentasListView,VentasUpdateView,VentasDeleteView

urlpatterns = [
    path('list/',VentasListView.as_view(),name = 'ventas_list'),
    path('create/', VentasView.as_view(),name="venta_create"),
    path('update/<int:pk>/', VentasUpdateView.as_view(),name="venta_update"),
    path('delete/<int:pk>/', VentasDeleteView.as_view(),name="venta_delete"),
]
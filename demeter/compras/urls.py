from django.urls import path

from .views import ComprasView, ComprasListView, ComprasUpdateView, ComprasDeleteView

urlpatterns = [
    path('create/', ComprasView.as_view(),name="compra_create"),
    path('list/', ComprasListView.as_view(),name="compra_list"),
    path('update/<int:pk>/', ComprasUpdateView.as_view(),name="compra_update"),
    path('delete/<int:pk>/', ComprasDeleteView.as_view(),name="compra_delete"),
]
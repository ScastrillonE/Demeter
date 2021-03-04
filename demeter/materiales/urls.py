from django.urls import path
from .views import MaterialView,MaterialListView,MaterialUpdateView,MaterialDeleteView
urlpatterns = [
    path('create/', MaterialView.as_view(),name="material_create"),
    path('list/', MaterialListView.as_view(), name="material_list"),
    path('update/<int:pk>/', MaterialUpdateView.as_view(), name="material_update"),
    path('delete/<int:pk>/', MaterialDeleteView.as_view(), name="material_delete"),
]
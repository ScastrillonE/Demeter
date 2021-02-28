from django.urls import  path

from .views import ClientView,ClientListView,ClientUpdateView,ClientDeleteView

urlpatterns = [
    path('registro/', ClientView.as_view(),name="register_client"),
    path('list/', ClientListView.as_view(), name="list_client"),
    path('update/<int:pk>/', ClientUpdateView.as_view(), name="update_client"),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name="delete_client"),
]
from django.urls import path, re_path
from .views import homeView, listClient, data_client

urlpatterns = [
    path('',homeView,name='bonificacion_home'),
    path('lista/', listClient,name="client_list_ajax"),
    path('data/client/', data_client,name= "data_client")
]
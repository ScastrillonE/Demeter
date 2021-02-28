from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ClientesConfig(AppConfig):
    name = 'demeter.clientes'
    verbose_name = 'clientes'
    label = 'Clientes'
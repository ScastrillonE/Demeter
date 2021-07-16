from django.db import models
from django.forms.models import model_to_dict

# Create your models here.

class Client(models.Model):
    name = models.CharField('Nombre', max_length = 150)
    identification = models.CharField('Cedula',max_length=90)
    phone = models.CharField('Telefono',max_length=90)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name}"

    def toJson(self):
        data = model_to_dict(self)

        return data
    
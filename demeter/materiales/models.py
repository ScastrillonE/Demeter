from django.db import models
from django.forms.models import model_to_dict


# Create your models here.
class Material(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    def toJson(self):
        data = model_to_dict(self)
        return data
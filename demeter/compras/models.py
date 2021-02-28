from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.forms.models import model_to_dict
from django.utils import timezone

from demeter.clientes.models import Client 
# Create your models here.
BONUS_CHOICES = [
    ('No_aplica','No aplica'),
    ('Carton','Carton'),
    ('Archivo','Archivo'),
    ('Periodico','Periodico'),
    ('Plega','Plega'),
    ('Plastico','Plastico'),
    ('Chatarra','Chatarra'),
    ('Vidrio','Vidrio'),
    ('Otros','Otros')
]
class Compra(models.Model):
    client_name = models.ForeignKey(Client, on_delete=models.CASCADE)
    material = models.CharField('Nombre material', max_length=150)
    kilos = models.CharField('Kilos',max_length=160)
    unit_value = models.CharField('Valor unitario',max_length=160)
    total_value = models.CharField('Total',max_length=160)
    creation_date = models.DateField('Fecha creacion')
    modified= models.DateField('Fecha modificacion')
    active = models.BooleanField(default=True)
    bonus = models.CharField(choices=BONUS_CHOICES, max_length=100,default='No_aplica')

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.creation_date = timezone.now()
        self.modified = timezone.now()
        return super(Compra, self).save(*args, **kwargs)

    def toJson(self):
        data = []
        data = model_to_dict(self)
        data['client'] = model_to_dict(self.client_name)

        return data

@receiver(pre_save, sender=Compra)
def calculate_total(sender,instance,**kwargs):
        instance.total_value = float(instance.unit_value) * float(instance.kilos)
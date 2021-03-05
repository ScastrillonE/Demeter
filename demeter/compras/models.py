from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.forms.models import model_to_dict
from django.utils import timezone

from demeter.clientes.models import Client
from demeter.materiales.models import Material
# Create your models here.
""" BONUS_CHOICES = [
    (0,'No aplica'),
    (1,'Carton'),
    (2,'Archivo'),
    (3,'Periodico'),
    (4,'Plega'),
    (5,'Plastico'),
    (6,'Chatarra'),
    (7,'Vidrio'),
    (8,'Otros')
] """

class Compra(models.Model):
    client_name = models.ForeignKey(Client, on_delete=models.CASCADE)
    total_value = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    creation_date = models.DateField('Fecha creacion',blank=True,null=True)
    modified= models.DateField('Fecha modificacion',blank=True,null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.creation_date = timezone.now()
        self.modified = timezone.now()
        return super(Compra, self).save(*args, **kwargs)

    def toJson(self):
        data = model_to_dict(self)
        data['client'] = model_to_dict(self.client_name)

        return data

class DetCompra(models.Model):
    compra = models.ForeignKey(Compra,on_delete=models.CASCADE,related_name='compratodet')
    material = models.ForeignKey(Material,on_delete=models.CASCADE)
    kilos = models.CharField('Kilos',max_length=160)
    unit_value = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    bonus = models.IntegerField(default=0)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    creation_date = models.DateField('Fecha creacion',blank=True,null=True)
    modified= models.DateField('Fecha modificacion',blank=True,null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.creation_date = timezone.now()
        self.modified = timezone.now()
        return super(DetCompra, self).save(*args, **kwargs)

    def toJson(self):
        data = model_to_dict(self)
        data['compra'] = model_to_dict(self.compra)

        return data

class Representation(models.Model):
    compraRepresentation = models.ForeignKey(Compra,on_delete=models.CASCADE,related_name='representa')
    representation = models.CharField(max_length=999,blank=True,null=True)

@receiver(pre_save, sender=DetCompra)
def calculate_total(sender,instance,**kwargs):
        Compra.total_value = float(instance.unit_value) * float(instance.kilos)

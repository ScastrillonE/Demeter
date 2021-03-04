from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone

from demeter.materiales.models import Material
# Create your models here.

class Ventas(models.Model):
    buyer = models.CharField('Empresa a la que vende',max_length=250)
    purchase = models.CharField('Empresa a la que compra',max_length=200)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    creation_date = models.DateField(blank=True,null=True)
    modified = models.DateField(blank=True,null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.creation_date = timezone.now()
        self.modified = timezone.now()
        return super(Ventas, self).save(*args, **kwargs)

    def toJson(self):
        data = []
        data = model_to_dict(self)

        return data

class DetVenta(models.Model):
    venta = models.ForeignKey(Ventas,on_delete=models.CASCADE,related_name='rn_venta')
    material = models.ForeignKey(Material,on_delete=models.CASCADE)
    kilos = models.CharField('Kilos',max_length=200)
    unit_value = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

class Representation(models.Model):
    ventaRepresentation = models.ForeignKey(Ventas,on_delete=models.CASCADE,related_name='representa')
    representation = models.CharField(max_length=999,blank=True,null=True)

from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone

# Create your models here.
class Ventas(models.Model):
    buyer = models.CharField('Empresa a la que vende',max_length=250)
    material = models.CharField('Material',max_length=250)
    kilos = models.CharField('Kilos',max_length=200)
    unit_value = models.CharField('Valor unitario',max_length=200)
    purchase = models.CharField('Empresa a la que compra',max_length=200)
    create = models.DateField(blank=True)

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
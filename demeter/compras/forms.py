from django import forms
from .models import Compra, DetCompra

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        exclude = ['creation_date','modified']

    def __init__(self,*args,**kwargs):
        super(CompraForm,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})

class DetCompraForm(forms.ModelForm):
    class Meta:
        model = DetCompra
        exclude = ['creation_date','modified']

    def __init__(self,*args,**kwargs):
        super(DetCompraForm,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})
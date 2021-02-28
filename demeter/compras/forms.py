from django import forms
from .models import Compra

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        exclude = ['active','creation_date','modified']

    def __init__(self,*args,**kwargs):
        super(CompraForm,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})
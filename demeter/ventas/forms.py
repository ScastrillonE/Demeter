from django import forms

from .models import Ventas

class VentasForm(forms.ModelForm):
    class Meta:
        model = Ventas
        fields = '__all__'
        exclude = ('create',)

    def __init__(self,*args,**kwargs):
        super(VentasForm,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})
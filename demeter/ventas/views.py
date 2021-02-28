from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DeleteView

from .forms import VentasForm
from .models import Ventas

# Create your views here.

class VentasView(LoginRequiredMixin,CreateView):
    model = Ventas
    form_class = VentasForm
    template_name = 'ventas/venta_create.html'
    success_url = reverse_lazy('venta_create')

class VentasListView(LoginRequiredMixin,ListView):
    model=Ventas
    template_name = 'ventas/venta_list.html'

    def get(self,request,*arg,**kwargs):
        if request.is_ajax():
            data = []
            for i in Ventas.objects.all():
                data.append(i.toJson())
            print(data)
            return JsonResponse(data, safe=False)
        else:
            return render(request, self.template_name)

class VentasUpdateView(LoginRequiredMixin,UpdateView):
    model = Ventas
    form_class = VentasForm
    template_name = 'ventas/venta_create.html'
    success_url = reverse_lazy('venta_create')
    
class VentasDeleteView(LoginRequiredMixin,DeleteView):
    model = Ventas
    success_url = reverse_lazy('venta_list')
    template_name = 'ventas/delete.html'
    context_object_name = 'obj'

    def delete(self,request,*args,**kwargs):
        self.object = self.model.objects.get(id=self.kwargs['pk'])
        self.object.active = False
        self.object.save()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)
        
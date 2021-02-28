from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DeleteView

from .forms import CompraForm
from .models import Compra

# Create your views here.

class ComprasView(LoginRequiredMixin,CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compras/compra_create.html'
    success_url = reverse_lazy('compra_create')

class ComprasListView(LoginRequiredMixin,ListView):
    model=Compra
    template_name = 'compras/compras_list.html'

    def get(self,request,*arg,**kwargs):
        if request.is_ajax():
            data = []
            for i in Compra.objects.filter(active=True):
                data.append(i.toJson())
                print(data)
            return JsonResponse(data, safe=False)
        else:
            return render(request, self.template_name)

class ComprasUpdateView(LoginRequiredMixin,UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compras/compra_create.html'
    success_url = reverse_lazy('compra_create')
    
class ComprasDeleteView(LoginRequiredMixin,DeleteView):
    model = Compra
    success_url = reverse_lazy('list_Compra')
    template_name = 'compras/delete.html'
    context_object_name = 'obj'

    def delete(self,request,*args,**kwargs):
        self.object = self.model.objects.get(id=self.kwargs['pk'])
        self.object.active = False
        self.object.save()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)
        
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DeleteView

from .forms import MaterialForm
from .models import Material

# Create your views here.

class MaterialView(LoginRequiredMixin,CreateView):
    model = Material
    form_class = MaterialForm
    template_name = 'materiales/create.html'
    success_url = reverse_lazy('material_create')

class MaterialListView(LoginRequiredMixin,ListView):
    model=Material
    template_name = 'materiales/material_list.html'

    def get(self,request,*arg,**kwargs):
        if request.is_ajax():
            data = []
            for i in Material.objects.all():
                data.append(i.toJson())
            return JsonResponse(data, safe=False)
        else:
            return render(request, self.template_name)

class MaterialUpdateView(LoginRequiredMixin,UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = 'materiales/create.html'
    success_url = reverse_lazy('material_create')
    
class MaterialDeleteView(LoginRequiredMixin,DeleteView):
    model = Material
    success_url = reverse_lazy('material_list')
    template_name = 'materiales/delete.html'
    context_object_name = 'obj'

    def delete(self,request,*args,**kwargs):
        self.object = self.model.objects.get(id=self.kwargs['pk'])
        self.object.active = False
        self.object.save()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)
        
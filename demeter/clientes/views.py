from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DeleteView

from .forms import ClientForm
from .models import Client

# Create your views here.

class ClientView(LoginRequiredMixin,CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clientes/register.html'
    success_url = reverse_lazy('register_client')

class ClientListView(LoginRequiredMixin,ListView):
    model=Client
    template_name = 'clientes/client_list.html'

    def get(self,request,*arg,**kwargs):
        if request.is_ajax():
            data = []
            for i in Client.objects.all():
                data.append(i.toJson())
                print(data)
            return JsonResponse(data, safe=False)
        else:
            return render(request, self.template_name)

class ClientUpdateView(LoginRequiredMixin,UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clientes/register.html'
    success_url = reverse_lazy('register_client')
    
class ClientDeleteView(LoginRequiredMixin,DeleteView):
    model = Client
    success_url = reverse_lazy('list_client')
    template_name = 'clientes/delete.html'
    context_object_name = 'obj'

    def delete(self,request,*args,**kwargs):
        self.object = self.model.objects.get(id=self.kwargs['pk'])
        self.object.active = False
        self.object.save()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)
        
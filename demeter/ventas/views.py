import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect,HttpResponse
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DeleteView, View

from django.core.serializers.json import DjangoJSONEncoder # Solucion error object decimal al convertir a formato json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from datetime import datetime
from demeter.materiales.models import Material
from .forms import VentasForm
from .models import Ventas,DetVenta,Representation

# Create your views here.

class VentasView(LoginRequiredMixin,CreateView):
    model = Ventas
    form_class = VentasForm
    template_name = 'ventas/venta_create.html'
    success_url = reverse_lazy('venta_create')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        now = datetime.now()
        context['time_now'] = now.strftime("%Y-%m-%d")
        context['title'] = "Agregar venta"
        context['action'] = 'save'

        return context

    def post(self,request,*args,**kwargs):
        data = []
        if request.is_ajax():
            data = []
            action = request.POST['action']
            if action == 'search_materiales':
                for i in Material.objects.filter(name__icontains = request.POST['term']):
                    data.append(i.toJson())
            return JsonResponse(data, safe=False)
        else:
            action = request.POST['action']
            if action == 'save':
                datos = json.loads(request.POST['datos'])
                print(datos)
                try:
                    with transaction.atomic():
                        venta = Ventas()
                        venta.buyer = datos['vende']
                        venta.purchase = datos['compra']
                        venta.total_value = datos['total']
                        venta.save()
                        
                        for material in datos['material']:

                            detalle_venta = DetVenta()
                            material_id = Material.objects.get(id=material['id'])

                            detalle_venta.venta = venta
                            detalle_venta.material =  material_id
                            detalle_venta.kilos = material['kilos']
                            detalle_venta.unit_value = material['valor_uni']
                            detalle_venta.total = material['total']
                            detalle_venta.save()
                        
                        representation = Representation()
                        representation.ventaRepresentation = venta
                        representation.representation = request.POST['representation']
                        representation.save()

                        data.append({'success':'Guardado con exito'})
                except Exception as e:
                    data.append({'error': str(e)})


            else:
                return JsonResponse(data, safe=False)

        return JsonResponse(data, safe=False)
        
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
 
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'
        context['det'] = Representation.objects.get(ventaRepresentation_id = self.kwargs['pk']).representation #json.dumps(self.get_det_compra(), cls=DjangoJSONEncoder)
        return context        
    
    def post(self,request,*args,**kwargs):
        data = []
        data_info ={}
        if request.is_ajax():
            data = []
            action = request.POST['action']
            if action == 'search_materiales':
                for i in Material.objects.filter(name__icontains = request.POST['term']):
                    data.append(i.toJson())
            return JsonResponse(data, safe=False)
        else:
            action = request.POST['action']
            if action == 'update':
                datos = json.loads(request.POST['datos'])
                print(datos)
                try:
                    with transaction.atomic():
                        venta = Ventas.objects.get(pk=self.kwargs['pk'])
                        venta.buyer =datos['vende']
                        venta.purchase = datos['compra']
                        venta.total_value = datos['total']
                        venta.save()

                        venta.rn_venta.all().delete()
                        for material in datos['material']:

                            detalle_venta = DetVenta()
                            material_id = Material.objects.get(id=material['id'])

                            detalle_venta.venta = venta
                            detalle_venta.material =  material_id
                            detalle_venta.kilos = material['kilos']
                            detalle_venta.unit_value = material['valor_uni']
                            detalle_venta.total = material['total']
                            detalle_venta.save()

                        venta.representa.all().delete()
                        representation = Representation()
                        representation.ventaRepresentation = venta
                        representation.representation = request.POST['representation']
                        representation.save()

                        data_info['success']='Actualizado con exito'
                except Exception as e:
                    print(e)
                    data_info['error'] = e


            else:
                return JsonResponse(data, safe=False)

        return JsonResponse(data, safe=False)
    
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
        
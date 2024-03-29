import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DeleteView, View

from django.core.serializers.json import DjangoJSONEncoder  # Solucion error object decimal al convertir a formato json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from datetime import datetime
from .forms import CompraForm, DetCompraForm
from .models import Compra, DetCompra, Representation
from demeter.materiales.models import Material
from demeter.clientes.models import Client

# xhtml2pdf
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
# Create your views here.


class ComprasView(LoginRequiredMixin, CreateView):
    model = Compra
    form_class = DetCompraForm
    template_name = 'compras/compra_create.html'
    success_url = reverse_lazy('compra_create')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = datetime.now()
        context['time_now'] = now.strftime("%Y-%m-%d")
        context['title'] = "Agregar compra"
        context['action'] = 'save'

        return context

    def post(self, request, *args, **kwargs):
        data = []
        data_info = {}
        if request.is_ajax():
            data = []
            action = request.POST['action']
            if action == 'search_materiales':
                for i in Material.objects.filter(name__icontains=request.POST['term']):
                    data.append(i.toJson())
            elif action == 'search_clients':
                for i in Client.objects.filter(name__icontains=request.POST['term']):
                    data.append(i.toJson())
            return JsonResponse(data, safe=False)
        else:
            action = request.POST['action']
            if action == 'save':
                datos = json.loads(request.POST['datos'])
                try:
                    with transaction.atomic():
                        cliente = Client.objects.get(id=datos['cliente'])
                        compra = Compra()
                        compra.client_name = cliente
                        compra.total_value = datos['total']
                        compra.save()

                        for material in datos['material']:

                            detalle_compra = DetCompra()
                            material_id = Material.objects.get(id=material['id'])
                            detalle_compra.compra = compra
                            detalle_compra.material = material_id
                            detalle_compra.kilos = material['kilos']
                            detalle_compra.unit_value = material['valor_uni']
                            detalle_compra.bonus = self.validar_bonus(material_id)
                            detalle_compra.total = material['total']
                            detalle_compra.save()

                        representation = Representation()
                        representation.compraRepresentation = compra
                        representation.representation = request.POST['representation']
                        representation.save()

                        data_info['success'] = 'Guardado con exito'
                        data_info['id_guardado'] = compra.id
                except Exception as e:
                    data_info['error'] = str(e)

            else:
                return JsonResponse(data_info, safe=False)

        return JsonResponse(data_info, safe=False)

    def validar_bonus(self, name):
        if str(name) == 'CARTON':
            return 1
        elif str(name) == 'ARCHIVO':
            return 2
        elif str(name) == 'PERIODICO':
            return 3
        elif str(name) == 'PLEGA':
            return 4
        elif str(name) == 'PLASTICO':
            return 5
        elif str(name) == 'CHATARRA':
            return 6
        elif str(name) == 'VIDRIO':
            return 7
        elif str(name) == 'PASTA GRUESA':
            return 8
        elif str(name) == 'PASTA REVUELTA':
            return 8

        return 0


class ComprasListView(LoginRequiredMixin, ListView):
    model = Compra
    template_name = 'compras/compras_list.html'

    def get(self, request, *arg, **kwargs):
        if request.is_ajax():
            data = []
            for i in Compra.objects.all():
                data.append(i.toJson())

            return JsonResponse(data, safe=False)
        else:
            return render(request, self.template_name)


class ComprasUpdateView(LoginRequiredMixin, UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compras/compra_create.html'
    success_url = reverse_lazy('compra_create')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'
        # json.dumps(self.get_det_compra(), cls=DjangoJSONEncoder)
        pre = Representation.objects.get(compraRepresentation_id=self.kwargs['pk']).representation
        pre = json.loads(pre)

        for i in pre["material"]:
            i["name"] = str(Material.objects.get(id=i["id"]))

        context['det'] = json.dumps(pre)

        return context

    def post(self, request, *args, **kwargs):
        data = []
        data_info = {}
        if request.is_ajax():
            data = []
            action = request.POST['action']
            if action == 'search_materiales':
                for i in Material.objects.filter(name__icontains=request.POST['term']):
                    data.append(i.toJson())
            elif action == 'search_clients':
                for i in Client.objects.filter(name__icontains=request.POST['term']):
                    data.append(i.toJson())
            return JsonResponse(data, safe=False)
        else:
            action = request.POST['action']
            if action == 'update':
                datos = json.loads(request.POST['datos'])
                try:
                    with transaction.atomic():
                        cliente = Client.objects.get(id=datos['cliente'])
                        compra = Compra.objects.get(pk=self.kwargs['pk'])
                        compra.client_name = cliente
                        compra.total_value = datos['total']
                        compra.save()

                        # compra.compratodet.all().delete()
                        detalle = DetCompra.objects.filter(compra=compra)
                        detalle.delete()
                        for material in datos['material']:

                            detalle_compra = DetCompra()
                            material_id = Material.objects.get(id=material['id'])

                            detalle_compra.compra = compra
                            detalle_compra.material = material_id
                            detalle_compra.kilos = material['kilos']
                            detalle_compra.unit_value = material['valor_uni']
                            detalle_compra.bonus = self.validar_bonus(material_id)
                            detalle_compra.total = material['total']

                            detalle_compra.save()

                        # compra.representa.all().delete()
                        represen = Representation.objects.filter(compraRepresentation=compra)
                        represen.delete()
                        representation = Representation()
                        representation.compraRepresentation = compra
                        representation.representation = request.POST['representation']
                        representation.save()

                        data_info['success'] = 'Actualizado con exito'
                        data_info['id_guardado'] = compra.id

                except Exception as e:
                    data_info['error'] = e

            else:
                return JsonResponse(data_info, safe=False)

        return JsonResponse(data_info, safe=False)


    def validar_bonus(self, name):
        if str(name) == 'CARTON':
            return 1
        elif str(name) == 'ARCHIVO':
            return 2
        elif str(name) == 'PERIODICO':
            return 3
        elif str(name) == 'PLEGA':
            return 4
        elif str(name) == 'PLASTICO':
            return 5
        elif str(name) == 'CHATARRA':
            return 6
        elif str(name) == 'VIDRIO':
            return 7
        elif str(name) == 'PASTA GRUESA':
            return 8
        elif str(name) == 'PASTA REVUELTA':
            return 8

        return 0


class ComprasDeleteView(LoginRequiredMixin, DeleteView):
    model = Compra
    success_url = reverse_lazy('compra_list')
    template_name = 'compras/delete.html'
    context_object_name = 'obj'


""" 
    def delete(self,request,*args,**kwargs):
        self.object = self.model.objects.get(id=self.kwargs['pk'])
        self.object.active = False
        self.object.save()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url) """


class CompraInvoicePrintView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        #import babel.numbers
        context = {}
        query = DetCompra.objects.filter(compra_id=self.kwargs['pk'])
        query_compra = Compra.objects.get(id=self.kwargs['pk'])
        context['data'] = query
        context['total'] = int(query_compra.total_value)
        context['fecha'] = query_compra.creation_date
        context['client'] = query_compra.client_name
        context['doc'] = query_compra.client_name.identification

        return render(request, 'compras/invoice.html', context=context)


class CompraInvoiceView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        query = DetCompra.objects.filter(compra_id=self.kwargs['pk'])
        query_compra = Compra.objects.get(id=self.kwargs['pk'])
        template = get_template('compras/invoice.html')
        print(query_compra.total_value)
        context['data'] = query
        context['total'] = int(query_compra.total_value)
        context['fecha'] = query_compra.creation_date
        context['client'] = query_compra.client_name
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'

        # create a pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

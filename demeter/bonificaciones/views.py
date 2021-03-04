import arrow
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from datetime import datetime, timedelta


from demeter.compras.models import Compra, DetCompra
from demeter.clientes.models import Client

# Create your views here.


def homeView(request):
    context = {}
    if request.method == 'GET':
        template_name = 'bonificaciones/index.html'
        return render(request,template_name)

@csrf_exempt
def listClient(request):

    if request.method == 'POST':
        data = []

        if request.is_ajax():
            for i in Client.objects.filter(Q(name__icontains=request.POST['search'])):
                data.append(i.toJson())
        else:
            data = 'Sin datos'
        
        return JsonResponse(data, safe=False)  

def data_client(request):

    if request.method == 'POST':
        kilos_carton = 0
        kilos_archivo = 0
        kilos_periodico = 0
        kilos_plega = 0
        kilos_plastico = 0
        kilos_chatarra = 0
        kilos_vidrio = 0
        kilos_otros = 0
        data = []

        
        query = Compra.objects.filter(client_name__id = request.POST['client_id'])
        j=0
        for j in range(0,len(query)):
            querydet = DetCompra.objects.filter(compra = query[j]).exclude(bonus=0)

            for i in querydet:
                
                if i.bonus == 1:
                    kilos_carton = kilos_carton + float(i.kilos)
                elif i.bonus == 2:
                    kilos_archivo = kilos_archivo + float(i.kilos)
                elif i.bonus == 3:
                    kilos_periodico = kilos_periodico + float(i.kilos)
                elif i.bonus == 4:
                    kilos_plega = kilos_plega + float(i.kilos)
                elif i.bonus == 5:
                    kilos_plastico= kilos_plastico + float(i.kilos)
                elif i.bonus == 6:
                    kilos_chatarra = kilos_chatarra + float(i.kilos)
                elif i.bonus == 7:
                    kilos_vidrio = kilos_vidrio + float(i.kilos)
                elif i.bonus == 8:
                    kilos_otros = kilos_otros + float(i.kilos)

        print(kilos_carton)
        data.append({'carton':format(float(kilos_carton), '0,.3f'),'archivo':format(float(kilos_archivo), '0,.3f'),'periodico':format(float(kilos_periodico), '0,.3f'),
        'plega':format(float(kilos_plega), '0,.3f'),'plastico':format(float(kilos_plastico), '0,.3f'),'chatarra':format(float(kilos_chatarra), '0,.3f'),'vidrio':format(float(kilos_vidrio), '0,.3f'),
        'otros':format(float(kilos_otros), '0,.3f')})
        
        
        return JsonResponse(data, safe=False)
        
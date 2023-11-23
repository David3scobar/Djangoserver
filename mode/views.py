import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mode.models import *
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect
from .forms import FiltroInformeForm
from django.contrib.admin.views.decorators import staff_member_required
from itertools import cycle
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from datetime import datetime
from django.utils import timezone
from django.db.models import Q
from django.utils.timezone import make_aware, now



def servicios(request):
    servicios_disponibles = Servicio.objects.all()
    return render(request, 'servicios.html', {'servicios': servicios_disponibles})


def reservas(request):
    return render(request, 'reservas.html')

def ingreso_productos_view(request):
    if request.method == 'POST':
        # Procesar el formulario si se ha enviado
        form = IngresoProductosForm(request.POST)
        if form.is_valid():
            form.save()
            # Realizar alguna acción después de guardar el formulario

    else:
        # Mostrar el formulario en una solicitud GET
        form = IngresoProductosForm()

    context = {'form': form}
    return render(request, 'rproveedor.html', context)


def crear_reserva(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        servicio_id = request.POST.get('servicio_id')
        rut = request.POST.get('rut')
        nombre = request.POST.get('nombre')

        # Restricción para fechas y horas
        fecha_hora_str = f'{fecha} {hora}'
        fecha_hora_naive = datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M')
        fecha_hora = make_aware(fecha_hora_naive)

        ahora = now()

        if fecha_hora < ahora:
            return JsonResponse({'message': 'La fecha y hora deben ser futuras.', 'error': True})

        # Verificar si ya existe una reserva para la misma fecha, hora y servicio
        reserva_existente = Reserva.objects.filter(
            Q(fecha_hora__gte=fecha_hora - timezone.timedelta(minutes=30)) &
            Q(fecha_hora__lte=fecha_hora + timezone.timedelta(minutes=30)),
            servicio_id=servicio_id
        ).exists()

        if reserva_existente:
            return HttpResponse('Ya hay una reserva para ese horario con otro servicio.', status=400)

        # Verificar si hay una reserva para el mismo servicio en la misma fecha y hora
        reserva_otro_servicio = Reserva.objects.filter(
            Q(fecha_hora__gte=fecha_hora - timezone.timedelta(minutes=30)) &
            Q(fecha_hora__lte=fecha_hora + timezone.timedelta(minutes=30)),
            servicio_id=servicio_id
        )

        if reserva_otro_servicio:
            return HttpResponse('Ya hay una reserva para ese horario con otro servicio.', status=400)

        servicio = Servicio.objects.get(id=servicio_id)
        estado = Estado.objects.get(id=1)

        # Obtener el usuario o establecer un usuario anónimo si no está autenticado
        usuario = request.user if request.user.is_authenticated else AnonymousUser()

        if usuario.is_authenticated:
            cliente_id = usuario.id
        else:
            # ID 4 para el cliente anónimo
            cliente_id = 4

        fecha_hora = make_aware(fecha_hora_naive)

        reserva = Reserva.objects.create(
            cliente_id=cliente_id,
            servicio=servicio,
            fecha_hora=fecha_hora,
            estado=estado,
            rut=rut,
            nombre=nombre
        )

        return render(request, 'home.html')


    # Resto del código para manejar otros casos si es necesario (GET)
    return render(request, 'tu_template.html')



def registro_factura_view(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar la factura en la base de datos
            return redirect('nombre_de_tu_vista_exitosa')  # Redirigir a una vista de éxito o a donde desees
    else:
        form = FacturaForm()
    
    context = {'form': form}
    return render(request, 'boletiar.html', context)


def registro_factura_view(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST, productos=Producto.objects.all(), servicios=Servicio.objects.all())
        if form.is_valid():
            form.save()
            return redirect('nombre_de_tu_vista_exitosa')
    else:
        form = FacturaForm(productos=Producto.objects.all(), servicios=Servicio.objects.all())

    context = {'form': form}
    return render(request, 'boletiar.html', context)

def listar_ordenes(request):
    ordenes = OrdenDePedido.objects.all()
    return render(request, 'ordenes_de_pedido/lista_ordenes.html', {'ordenes': ordenes})

def crear_orden(request):
    if request.method == 'POST':
        form = OrdenDePedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_ordenes')
    else:
        form = OrdenDePedidoForm()

    usuarios = User.objects.all()  # Recuperar todos los usuarios
    productos = Producto.objects.all()  # Recuperar todos los productos

    return render(request, 'ordenes_de_pedido/formulario_orden.html', {'form': form, 'usuarios': usuarios, 'productos': productos})





def editar_orden(request, orden_id):
    orden = get_object_or_404(OrdenDePedido, pk=orden_id)
    if request.method == 'POST':
        form = EditarOrdenDePedidoForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            return redirect('listar_ordenes')
    else:
        form = EditarOrdenDePedidoForm(instance=orden)

    return render(request, 'ordenes_de_pedido/editar_orden.html', {'form': form, 'orden': orden})



def informe_personalizado(request):
    if request.method == 'POST':
        form = FiltroInformeForm(request.POST)
        if form.is_valid():
            # Procesa los datos del formulario y genera el informe
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
            
            # Realiza consultas a los modelos según tus necesidades
            servicios = Servicio.objects.filter(fecha_hora__range=(fecha_inicio, fecha_fin))
            reservas = Reserva.objects.filter(fecha_hora__range=(fecha_inicio, fecha_fin))
            productos = Producto.objects.all()
            ingresos = IngresoProductos.objects.filter(fecha_ingreso__range=(fecha_inicio, fecha_fin))
            facturas = Factura.objects.filter(fecha_emision__range=(fecha_inicio, fecha_fin))
            ordenes = OrdenDePedido.objects.filter(fecha_pedido__range=(fecha_inicio, fecha_fin))
            
            # Realiza cualquier otro procesamiento necesario para generar el informe
            # ...
            
            return render(request, 'informe.html', {'servicios': servicios, 'reservas': reservas, 'productos': productos, 'ingresos': ingresos, 'facturas': facturas, 'ordenes': ordenes})
    else:
        form = FiltroInformeForm()

    return render(request, 'informe.html', {'form': form})



def home(request):
    # Lógica adicional si es necesaria
    return render(request, 'home.html')


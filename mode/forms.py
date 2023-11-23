from csv import reader
from django import forms
from .models import *
from django.shortcuts import render, get_object_or_404, redirect

class IngresoProductosForm(forms.ModelForm):
    class Meta:
        
        model = IngresoProductos
        fields = ['producto', 'proveedor', 'fecha_ingreso', 'cantidad']
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
        }

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['cliente', 'nombre', 'rut_cliente', 'es_producto', 'producto', 'servicio']

    def __init__(self, *args, **kwargs):
        productos = kwargs.pop('productos', None)
        servicios = kwargs.pop('servicios', None)
        super(FacturaForm, self).__init__(*args, **kwargs)

        self.fields['producto'] = forms.ModelChoiceField(
            queryset=productos,
            required=False,
            label='Producto'
        )
        self.fields['servicio'] = forms.ModelChoiceField(
            queryset=servicios,
            required=False,
            label='Servicio'
        )
        

    def clean(self):
        cleaned_data = super(FacturaForm, self).clean()
        tipo = cleaned_data.get('es_producto')

        if tipo == 'Producto':
            cleaned_data['servicio'] = None
        elif tipo == 'Servicio':
            cleaned_data['producto'] = None

        return cleaned_data

def registro_factura_view(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST, productos=Producto.objects.all(), servicios=Servicio.objects.all())
        if form.is_valid():
            form.save()
            #return redirect('nombre_de_tu_vista_exitosa')
    else:
        form = FacturaForm(productos=Producto.objects.all(), servicios=Servicio.objects.all())
    usuarios = User.objects.all()  # Ajusta esto para obtener los usuarios que deseas
    context = {'form': form, 'usuarios': usuarios}
     

    context = {'form': form}
    return reader(request, 'boletiar.html', context)


class OrdenDePedidoForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(queryset=User.objects.all(), label="Proveedor")
    productos = forms.ModelMultipleChoiceField(queryset=Producto.objects.all(), label="Productos", widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = OrdenDePedido
        fields = ['proveedor', 'productos', 'cantidad', 'estado_entrega']

class EditarOrdenDePedidoForm(forms.ModelForm):
    class Meta:
        model = OrdenDePedido
        fields = ['proveedor', 'productos', 'cantidad', 'estado_entrega']        

        
def eliminar_orden(request, orden_id):
    orden = get_object_or_404(OrdenDePedido, pk=orden_id)
    if request.method == 'POST':
        orden.delete()
        return redirect('listar_ordenes')  # Redirige a la lista de órdenes después de eliminar una orden

    return render(request, 'ordenes_de_pedido/eliminar_orden.html', {'orden': orden})


class FiltroInformeForm(forms.Form):
    fecha_inicio = forms.DateField(label='Fecha de inicio', required=False)
    fecha_fin = forms.DateField(label='Fecha de fin', required=False)
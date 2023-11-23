from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Servicio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
    
    
    
class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(default=timezone.now)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    
    rut = models.CharField(max_length=20)  # Ajusta el valor predeterminado según necesites
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Reserva de {self.cliente.username} para {self.servicio.nombre} el {self.fecha_hora}"


    

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    sku = models.CharField(max_length=20, unique=True)  # El campo SKU es único
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre    
    
class IngresoProductos(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField()
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f'Ingreso de {self.cantidad} {self.producto.nombre} por {self.proveedor.username}'    
    

class Factura(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    rut_cliente = models.CharField(max_length=20)
    es_producto = models.BooleanField()  # True para producto, False para servicio
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, null=True, blank=True)
    fecha_emision = models.DateField(auto_now_add=True)
    # Otros campos relacionados con la factura, como precio, cantidad, etc.

    def __str__(self):
        return f'Factura de {self.cliente.username} - {self.nombre}'    
    


class OrdenDePedido(models.Model):
    proveedor = models.ForeignKey(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)
    cantidad = models.PositiveIntegerField()
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado_entrega = models.BooleanField(default=False)
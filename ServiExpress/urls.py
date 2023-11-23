"""ServiExpress URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mode.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('servicios/', servicios, name='servicios'),
    path('reservas/', reservas, name='reservas'),
    path('crear_reserva/', crear_reserva, name='crear_reserva'),
    path('inventario/', ingreso_productos_view, name='registro_inventario'),
    path('boletiar/', registro_factura_view, name='registro_boletas'),
    path('listar/', listar_ordenes, name='listar_ordenes'),
    path('crear/', crear_orden, name='crear_orden'),
    path('editar/<int:orden_id>/', editar_orden, name='editar_orden'),
    path('eliminar/<int:orden_id>/', eliminar_orden, name='eliminar_orden'),
    path('informes', informe_personalizado, name='informes'),
    path('', home, name='home'),



]

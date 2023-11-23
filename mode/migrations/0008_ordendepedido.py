# Generated by Django 4.1.7 on 2023-10-20 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mode', '0007_factura'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenDePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True)),
                ('estado_entrega', models.BooleanField(default=False)),
                ('productos', models.ManyToManyField(to='mode.producto')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

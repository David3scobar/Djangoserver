# Generated by Django 4.1.7 on 2023-10-13 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mode', '0004_estado_rename_usuario_reserva_cliente_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('sku', models.CharField(max_length=20, unique=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]

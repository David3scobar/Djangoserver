# Generated by Django 4.1.7 on 2023-09-23 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mode', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
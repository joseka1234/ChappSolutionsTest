# Generated by Django 3.1.1 on 2020-09-24 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buscadorApp', '0004_auto_20200924_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='fecha_entrada',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='fecha_salida',
            field=models.DateField(),
        ),
    ]

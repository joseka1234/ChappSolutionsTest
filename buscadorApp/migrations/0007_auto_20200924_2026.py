# Generated by Django 3.1.1 on 2020-09-24 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buscadorApp', '0006_remove_reserva_n_habitacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='habitacion',
            name='n_habitaciones',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='NumeroHabitaciones',
        ),
    ]

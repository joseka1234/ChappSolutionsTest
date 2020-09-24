"""
Módulo que incluye la representación de una reserva en la BD.
"""

from django.db import models
from . import habitacion


class Reserva(models.Model):
    """
    Clase que representa una reserva en la base de datos.

    :param localizador: Localizador para la reserva

    :type localizador: CharField(max_length=15)

    :param fecha_entrada: Fecha de entrada para la reserva. Se establece por defecto al día actual.
    
    :type fecha_entrada: DateField

    :param fecha_salida: Fecha de salida parala reserva. Se establece por defecto al día actual.
    
    :type fecha_salida: DateField

    :param tipo_habitacion: Tipo de habitación de la reserva

    :type tipo_habitacion: ForeignKey(Habitacion)

    :param n_huespedes: Nº de huespedes de la reserva

    :type n_huespedes: IntegerField

    :param huesped_nombre: Nombre del huesped

    :type huesped_nombre: CharField(max_length=100)

    :param huesped_email: Email de contacto del huesped

    :type huesped_email: CharField(max_length=100)

    :param huesped_telefono: Teléfono de contacto del huesped

    :type huesped_telefono: CharField(max_length=30)

    :param precio_total: Precio total de la reserva

    :type precio_total: FloatField

    """
    id = models.AutoField(primary_key=True)
    localizador = models.CharField(max_length=15, null=False)
    fecha_entrada = models.DateField(null=False)
    fecha_salida = models.DateField(null=False)
    tipo_habitacion = models.ForeignKey(habitacion.Habitacion, on_delete=models.CASCADE, null=False)
    n_huespedes = models.IntegerField(null=False)
    huesped_nombre = models.CharField(max_length=100, null=False)
    huesped_email = models.EmailField(max_length=100, null=False)
    huesped_telefono = models.CharField(max_length=30, null=False)
    precio_total = models.FloatField()
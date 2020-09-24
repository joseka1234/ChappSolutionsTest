"""
Módulo que incluye la representación de las habitaciones que se pueden reservar.
"""

from django.db import models


class Habitacion(models.Model):
    """
    Clase que representa una habitación en el hotel.

    :param id: ID de la habitación

    :type id: AutoField

    :param tipo: Tipo de habitación (P.Ej.: Individual, Doble, Triple...)
    
    :type tipo: CharField
    
    :param precio: Precio de este tipo de habitación
    
    :type precio: FloatField
    
    :param n_habitaciones: Número de habitaciones de habitaciones que existen de un tipo.
    
    :type n_habitaciones: IntegerField

    :param capacidad: Capacidad de la habitación en número de personas.

    :type capacidad: IntegerField
    """

    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=15)
    precio = models.FloatField(default=0)
    n_habitaciones = models.IntegerField(default=0)
    capacidad = models.IntegerField(default=0)
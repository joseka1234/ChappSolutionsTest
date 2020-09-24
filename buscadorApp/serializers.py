"""
Módulo que contiene las clases de serialización para los modelos de Reserva y Habitacion.
"""

from .models.reserva import Reserva
from .models.habitacion import Habitacion
from rest_framework import serializers


class ReservaSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Reserva
        fields = (
            "id",
            "localizador",
            "fecha_entrada",
            "fecha_salida",
            "tipo_habitacion",
            "n_huespedes",
            "huesped_nombre",
            "huesped_email",
            "huesped_telefono",
            "precio_total",
            "n_habitacion",
        )
        

class HabitacionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Habitacion
        fields = (
            "id",
            "tipo",
            "precio",
            "cantidad",
            "capacidad",
        )
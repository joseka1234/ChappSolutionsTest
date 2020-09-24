from django.contrib import admin
from .models.reserva import Reserva
from .models.habitacion import Habitacion

# Register your models here.
admin.site.register(Reserva)
admin.site.register(Habitacion)
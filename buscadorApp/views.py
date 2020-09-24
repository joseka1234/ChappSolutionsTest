from django.db.models import Q
from django.conf import settings
from django.shortcuts import render, redirect
import datetime

from rest_framework import viewsets
from rest_framework import permissions

from .serializers import ReservaSerializer, HabitacionSerializer
from .models.reserva import Reserva
from .models.habitacion import Habitacion
from .forms.reserva_form import ReservaFechasForm, ReservaHabitacionForm


def lista_reservas(request):
    """
    Gestiona las llamadas a la url /.
    Renderiza la lista de reservas guardadas en la base de datos.
    """
    context = {
        'reservas': Reserva.objects.all()
    }
    return render(request, 'lista_reservas.html', context)


def __get_form_errors(form):
    """
    Comprueba los errores del formulario y devuelve una cadena texto o None en caso de que no exista ningún error.

    :returns: Error en formato str o None en caso de no haber ningún error.

    :rtype: str
    """
    fecha_entrada = form.cleaned_data.get('fecha_entrada')
    fecha_salida =  form.cleaned_data.get('fecha_salida')

    if (fecha_salida - fecha_entrada).days < 0:
        return "¡La fecha de salida no puede ser anterior a la de entrada!"

    if form.cleaned_data.get('n_huespedes') <= 0:
        # En principio esto no debería salir núnca
        return "Debe seleccionar al menos un huesped"

    return None


def __get_habitaciones_disponibles(form):
    """
    Devuelve el QuerySet que corresponde a las habitaciones disponibles entre las fechas incluidas en el formulario web.

    :return: Un diccionario que contiene como clave una habitación y como valor la cantidad de habitaciones disponibles de un tipo.

    :rtype: Dictionary {Habitacion: int}
    """

    habitaciones = Habitacion.objects.filter(capacidad__gte=form.cleaned_data.get('n_huespedes'))
    fecha_entrada = form.cleaned_data.get('fecha_entrada')
    fecha_salida = form.cleaned_data.get('fecha_salida')

    # Reservas con las que choca nuestra fecha de inicio también se tiene en cuenta que comiencen enl mismo día.
    # Reservado |-----------------| Fin Reserva
    #                    ^ Nuestra fecha de entrada
    fecha_inicio_invalida = Q(fecha_entrada__gte=fecha_entrada, fecha_entrada__lte=fecha_salida)

    # Reservas con las que choca nuestra fecha de fin también se tiene en cuenta que finalizen el mismo día.
    # Reservado |-----------------| Fin Reserva
    #                    ^ Nuestra fecha de salida
    fecha_fin_invalida = Q(fecha_salida__gte=fecha_entrada, fecha_salida__lte=fecha_salida)


    # Reservas que ocupan la habitación mientras estamos quedándonos en el hotel
    #             Reservado |-----------------| Fin Reserva
    # Nuestra Reserva |--------------------------------| Fin Reserva
    ocupado_en_medio = Q(fecha_entrada__lte=fecha_entrada, fecha_salida__gte=fecha_salida)

    fechas_invalidas = Reserva.objects.filter(fecha_inicio_invalida | fecha_fin_invalida | ocupado_en_medio)
    
    return {h: h.n_habitaciones - fechas_invalidas.filter(tipo_habitacion=h.id).count() for h in habitaciones}


def elegir_fecha(request):
    """
    Gestiona las llamadas a la url /elegir_fecha
    Renderiza el formulario para introducir las fechas deseadas.
    """
    form = ReservaFechasForm()

    if request.method == "POST":
        form = ReservaFechasForm(request.POST)

        if form.is_valid():
            fecha_entrada = form.cleaned_data.get('fecha_entrada')
            fecha_salida =  form.cleaned_data.get('fecha_salida')
            
            request.session['fecha_entrada'] = fecha_entrada.strftime(settings.FORMATO_FECHA_PRINCIPAL)
            request.session['fecha_salida'] = fecha_salida.strftime(settings.FORMATO_FECHA_PRINCIPAL)
            request.session['n_huespedes'] = form.cleaned_data.get('n_huespedes')

            context = {
                'fecha_seleccionada': 1,
                'reserva_fechas_form': form,
                'habitaciones': __get_habitaciones_disponibles(form),
                'dias_reserva': (fecha_salida - fecha_entrada).days,
            }
            
            return render(request, 'elegir_fecha.html', context)
        else:
            context = {
                'reserva_fechas_form': form,
                'error': __get_form_errors(form),
            }
            return render(request, 'elegir_fecha.html', context)


    
    context = {
        'reserva_fechas_form': form,
    }
    
    return render(request, 'elegir_fecha.html', context)


def __get_localizador(habitacion, reserva_id):
    """
    Devuelve el localizador de una reserva

    :return: Localizador de una reserva

    :rtype: str
    """
    return "{}{}{:05d}".format(datetime.date.today().year, habitacion.tipo[:1], reserva_id)
    

def reservar(request, id_habitacion):
    """
    Gestiona las llamadas a la url /reservar
    Renderiza el formulario para introducir los datos del cliente.
    """
    form = ReservaHabitacionForm()

    habitacion = Habitacion.objects.filter(id=id_habitacion).first()

    fecha_entrada = datetime.datetime.strptime(request.session['fecha_entrada'], settings.FORMATO_FECHA_PRINCIPAL)
    fecha_salida =  datetime.datetime.strptime(request.session['fecha_salida'], settings.FORMATO_FECHA_PRINCIPAL)

    dias = (fecha_salida - fecha_entrada).days
    subtotal = dias * habitacion.precio
    impuestos = (settings.IMPUESTO / 100) * subtotal
    total = subtotal + impuestos

    if request.method == "POST":
        form = ReservaHabitacionForm(request.POST)
        if form.is_valid():
            reserva = Reserva(
                fecha_entrada=fecha_entrada,
                fecha_salida=fecha_salida,
                tipo_habitacion=habitacion,
                n_huespedes=int(request.session['n_huespedes']),
                huesped_nombre=form.cleaned_data.get('nombre'),
                huesped_email=form.cleaned_data.get('email'),
                huesped_telefono=form.cleaned_data.get('telefono'),
                precio_total=total,
            )
            reserva.save()
            reserva.localizador = __get_localizador(habitacion=habitacion, reserva_id=reserva.id)
            reserva.save()
            
            return redirect('lista_reservas')

    context = {
        'reserva_habitacion_form': form,
        'n_huespedes': request.session['n_huespedes'],
        'dias': dias,
        'subtotal': subtotal,
        'impuestos': impuestos,
        'total': total,
    }

    return render(request, 'reservar.html', context)


class ReservaViewSet(viewsets.ModelViewSet):
    """
    Endpoint de la API que permite visualizar o editar las reservas
    """
    serializer_class = ReservaSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Reserva.objects.all()


class HabitacionViewSet(viewsets.ModelViewSet):
    """
    Endpoint de la API que permite visualizar o editar las habitaciones
    """
    serializer_class = HabitacionSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Habitacion.objects.all()
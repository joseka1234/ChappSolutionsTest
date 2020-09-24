"""
Formularios relacionados con la reserva de habitaciones.
"""

from ..models.reserva import Reserva

from django import forms
from django.conf import settings
import re


class ReservaFechasForm(forms.Form):
    """
    Formulario para seleccionar las fechas entre las cuales se va a buscar para reservar.
    
    :param fecha_entrada: Fecha en la que se entrará a la habitación
    
    :type fecha_entrada: DateField
    
    :param fecha_salida: Fecha en la que se saldrá de la habitación
    
    :type fecha_entrada: DateField
    """

    class Meta:
        model = Reserva
        fields = [
            "fecha_entrada ",
            "fecha_salida",
            "n_huespedes ",
        ]

    fecha_entrada = forms.DateField(input_formats=settings.FORMATO_FECHA, widget=forms.TextInput(attrs=
                                    {
                                        'class': 'form-control datepicker',
                                        'autocomplete': 'off',
                                        'placeholder': 'Fecha Entrada',
                                    }), required=True)

    fecha_salida = forms.DateField(input_formats=settings.FORMATO_FECHA, widget=forms.TextInput(attrs=
                                    {
                                        'class': 'form-control datepicker',
                                        'autocomplete': 'off',
                                        'placeholder': 'Fecha Salida',
                                    }), required=True)

    n_huespedes = forms.IntegerField(widget=forms.NumberInput(attrs=
                                    {
                                        'class': 'form-control',
                                        'placeholder': 'Nº Huespedes',
                                    }), required=True, min_value=1, max_value=99)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("fecha_salida") < cleaned_data.get("fecha_entrada"):
            msg = "¡La fecha de salida no puede ser anterior a la de entrada!"
            self._errors["fecha_salida"] = self.error_class([msg])


class ReservaHabitacionForm(forms.Form):
    """
    Formulario para reservar una habitación, con toda la información requerida.
    
    :param nombre: Nombre del huesped
    
    :type nombre: CharField
    
    :param email: Email del huesped

    :type email: EmailField

    :param telefono: Teléfono del huesped

    :type telefono:
    """

    class Meta:
        model = Reserva
        fields = [
            "nombre ",
            "email",
            "telefono ",
        ]

    nombre = forms.CharField(widget=forms.TextInput(attrs=
                            {
                                'class': 'form-control',
                                'placeholder': 'Ej: Paco Martínez',
                            }), required=True)

    email = forms.EmailField(widget=forms.EmailInput(attrs=
                            {
                                'class': 'form-control',
                                'placeholder': 'Ej: example@mail.com',
                            }), required=True)

    telefono = forms.CharField(widget=forms.TextInput(attrs=
                                {
                                    'class': 'form-control',
                                    'placeholder': 'Ej: +36 699-633-369',
                                    'pattern': '^\+?[0-9\s\-]+',
                                }), required=True)
    
    def clean(self):
        cleaned_data = super().clean()

        """
        if re.search(r"^.+@.+\..+$", cleaned_data.get("email")) == None:
            self._errors["email"] = self.error_class(["El email es inválido."])
        """
        
        if re.search(r"^\+?[0-9\s\-]+", cleaned_data.get("telefono")) == None:
            self._errors["email"] = self.error_class(["El teléfono es inválido."])
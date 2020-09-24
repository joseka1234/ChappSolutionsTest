from django.test import TestCase
from django.test import TestCase
from ..models.habitacion import Habitacion
from ..models.reserva import Reserva
from ..forms.reserva_form import ReservaFechasForm, ReservaHabitacionForm


class ReservaTestCase(TestCase):
    def setUp(self) -> None:
        Habitacion.objects.create(tipo="Individual", precio=25, n_habitaciones=6, capacidad=1)
        h_doble = Habitacion.objects.create(tipo="Doble", precio=46, n_habitaciones=15, capacidad=2)

        Reserva.objects.create(localizador="LOCALIZADOR", fecha_entrada="2020-06-25", fecha_salida="2020-06-30",
                                tipo_habitacion=h_doble, n_huespedes=1, huesped_nombre="Nombre", huesped_email="Email@email.com",
                                huesped_telefono="9595959595", precio_total=230.0)


    def test_lista_reservas(self):
        """
        Test para comprobar que la BD funciona correctamente.
        Se comprueba que exista al menos una reserva en la BD
        """
        self.assertEqual(Reserva.objects.all().count(), 1)

    
    def test_lista_habitaciones(self):
        """
        Test para comprobar que la BD funciona correctamente.
        Se comprueba que existan al menos dos habitaciones en la BD
        """
        self.assertEqual(Habitacion.objects.all().count(), 2)


    def test_form_fechas(self):
        """
        Test para comprobar que el formulario para introducir los datos de reserva funciona correctamente.
        """
        form_correcto = ReservaFechasForm(data={"fecha_entrada": "25/06/2020", "fecha_salida": "30/06/2020", "n_huespedes": 1})
        self.assertEqual(form_correcto.is_valid(), True)

        form_huespedes_incorrectos = ReservaFechasForm(data={"fecha_entrada": "25/06/2020", "fecha_salida": "30/06/2020", "n_huespedes": -1})
        self.assertEqual(form_huespedes_incorrectos.is_valid(), False)

        form_fechas_incorrectos = ReservaFechasForm(data={"fecha_entrada": "30/06/2020", "fecha_salida": "25/06/2020", "n_huespedes": 1})
        self.assertEqual(form_fechas_incorrectos.is_valid(), False)


    def test_form_reserva_habitacion(self):
        """
        Test para comprobar que el formulario para introducir los datos del huesped funciona correctamente.
        """
        form_correcto = ReservaHabitacionForm(data={"nombre": "Nombre", "email": "email@email.com", "telefono": "+34 694-35-36-65"})
        self.assertEqual(form_correcto.is_valid(), True)

        form_email_incorrecto = ReservaHabitacionForm(data={"nombre": "Nombre", "email": "emailemail.com", "telefono": "+34 694-35-36-65"})
        self.assertEqual(form_email_incorrecto.is_valid(), False)

        form_telefono_incorrecto = ReservaHabitacionForm(data={"nombre": "Nombre", "email": "emailemail.com", "telefono": "+34 asd"})
        self.assertEqual(form_telefono_incorrecto.is_valid(), False)


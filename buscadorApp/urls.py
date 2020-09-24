from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'reservas', views.ReservaViewSet)
router.register(r'habitaciones', views.HabitacionViewSet)

urlpatterns = [
    #API URLs
    path('api/', include(router.urls)),
    #Website URLs
    path('', views.lista_reservas, name='lista_reservas'),
    path('elegir_fecha', views.elegir_fecha, name='elegir_fecha'),
    path(r'reservar/<int:id_habitacion>', views.reservar, name='reservar')
]
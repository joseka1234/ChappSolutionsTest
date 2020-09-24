from django import template


register = template.Library()


@register.filter(name='multiply')
def multiply(value, arg):
    """
    Filtro para multiplicar dos valores y mostrarlos en pantalla.
    Se utilizará principalmente para calcular precios totales.
    """
    return value * arg
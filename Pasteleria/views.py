from django.shortcuts import render
from .models import Producto
def inicio(request):
    productos = Producto.objects.select_related('linea').filter(disponible=True)
    return render(request, 'catalogo/inicio.html', {'productos': productos})
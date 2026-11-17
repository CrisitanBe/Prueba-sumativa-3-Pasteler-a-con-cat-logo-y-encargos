
from django.shortcuts import render, get_object_or_404
from .models import Producto, Linea
def inicio(request):
    productos = Producto.objects.select_related('linea').filter(disponible=True)
    linea = request.GET.get('linea')
    if linea:
        productos = productos.filter(linea__id=linea)
    q = request.GET.get('q')    
    if q:
        productos = productos.filter(nombre__icontains=q)
    return render(request, 'catalogo/inicio.html', {
    'productos': productos,'lineas': Linea.objects.all(),
})
def detalle(request, id):
    producto = get_object_or_404(
        Producto.objects.select_related('linea'),
        id=id, disponible=True)
    return render(request, 'catalogo/detalle.html', {'producto': producto})
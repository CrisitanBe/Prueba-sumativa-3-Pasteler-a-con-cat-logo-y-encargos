from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Linea, Encargo
from .forms import EncargoForm


def inicio(request):
    productos = Producto.objects.select_related('linea').filter(disponible=True)
    linea = request.GET.get('linea')
    if linea:
        productos = productos.filter(linea__id=linea)
    q = request.GET.get('q')
    if q:
        productos = productos.filter(nombre__icontains=q)
    return render(request, 'catalogo/inicio.html', {
        'productos': productos,
        'lineas': Linea.objects.all(),
    })


def detalle(request, id):
    producto = get_object_or_404(Producto.objects.select_related('linea'),
    id=id, disponible=True)
    if request.method == 'POST' and not producto.agotado:
        form = EncargoForm(request.POST, producto=producto)
        if form.is_valid():
            encargo = form.save(commit=False)
            encargo.producto = producto
            encargo.save()
            producto.stock -= encargo.cantidad
            producto.save()
            messages.success(request, 'Encargo registrado.')
            return redirect('catalogo:comprobante', id=encargo.id)
    else:
        form = EncargoForm(producto=producto)
    return render(request, 'catalogo/detalle.html',{'producto': producto, 'form': form})

def comprobante(request, id):
    encargo = get_object_or_404(
        Encargo.objects.select_related('producto'), id=id)
    return render(request, 'catalogo/comprobante.html',{'encargo': encargo})
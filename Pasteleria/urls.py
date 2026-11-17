from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('producto/<int:id>/', views.detalle, name='detalle'),
    path('encargo/<int:id>/comprobante/', views.comprobante, name='comprobante'),
]
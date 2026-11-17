from django.contrib import admin
from django.utils.html import format_html
from .models import Linea, Producto, Encargo, formato_clp


@admin.register(Linea)
class LineaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'linea', 'disponible', 'stock','precio_pesos', 'apto_celiacos', 'miniatura')
    list_filter = ('linea', 'apto_celiacos')
    search_fields = ('nombre',)
    list_select_related = ('linea',)
    readonly_fields = ('miniatura',)
    @admin.display(description='Precio', ordering='precio')
    def precio_pesos(self, obj):
        return formato_clp(obj.precio)
    @admin.display(description='Foto')
    def miniatura(self, obj):
        return format_html('<img src="{}" style="height:60px; border-radius:4px;">',obj.foto_url)

@admin.register(Encargo)
class EncargoAdmin(admin.ModelAdmin):
    list_display = ('codigo_encargo', 'producto', 'nombre','cantidad', 'fecha_retiro')
    list_filter = ('producto', 'fecha_retiro')
    search_fields = ('nombre', 'email')
    list_select_related = ('producto',)
    @admin.display(description='Código', ordering='id')
    def codigo_encargo(self, obj):
        return obj.codigo
from django.db import models
from django.templatetags.static import static
def formato_clp(valor):
    return f"${valor:,}".replace(",", ".")
class Linea(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    class Meta:
        ordering = ['nombre']
        verbose_name = 'línea'
        verbose_name_plural = 'líneas'
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    linea = models.ForeignKey(Linea, on_delete=models.CASCADE, related_name='productos')
    foto = models.ImageField(upload_to='productos/', blank=True, null=True)
    precio = models.PositiveIntegerField()
    porciones = models.PositiveSmallIntegerField()
    apto_celiacos = models.BooleanField(default=False, verbose_name='apto para celíacos')
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
    def __str__(self):
        return self.nombre
    @property
    def agotado(self):
        return self.stock == 0
    def precio_clp(self):
        return formato_clp(self.precio)
    @property
    def foto_url(self):
        if self.foto:
            return self.foto.url
        return static('img/sin-foto.png')
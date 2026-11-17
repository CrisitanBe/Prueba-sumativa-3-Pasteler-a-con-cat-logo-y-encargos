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
    linea = models.ForeignKey(
    Linea, on_delete=models.CASCADE, related_name='productos')
    foto = models.ImageField(upload_to='productos/', blank=True, null=True)
    precio = models.PositiveIntegerField()
    porciones = models.PositiveSmallIntegerField()
    apto_celiacos = models.BooleanField(
    default=False, verbose_name='apto para celíacos')
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


    
class Encargo(models.Model):
    producto = models.ForeignKey(
    Producto, on_delete=models.CASCADE, related_name='encargos')
    nombre = models.CharField(max_length=80)
    email = models.EmailField(verbose_name='correo')
    fecha_retiro = models.DateField(verbose_name='fecha de retiro')
    cantidad = models.PositiveIntegerField(default=1)
    creado = models.DateTimeField(
    auto_now_add=True, verbose_name='fecha y hora del encargo')
    class Meta:
        ordering = ['-creado']
    def __str__(self):
        return f"{self.codigo} · {self.nombre}"
    @property
    def codigo(self):
        return f"ENC-{self.id:05d}" if self.id else "ENC-nuevo"
    @property
    def total(self):
        return self.producto.precio * self.cantidad
    def total_clp(self):
        return formato_clp(self.total)
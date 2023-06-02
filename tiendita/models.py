from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.

class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager,self).get_queryset().filter(activo=True)

class Categoria(models.Model):
    nombre = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique= True)

    class Meta:
        verbose_name_plural = 'categorias'

    def get_absolute_url(self):
        return reverse('tiendita:categoria_lista', args=[self.slug])

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='producto',on_delete=models.CASCADE)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_creator')
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255, default='admin')
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='media/')
    slug = models.SlugField(max_length=255)
    precio = models.DecimalField(max_digits=7, decimal_places=3)
    en_stock = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    subido = models.DateTimeField(auto_now=True)
    aprobado = models.BooleanField(default= False) # pasara a ser revisado para mostrase con los demas productos
    objects = models.Manager()
    producto = ProductManager()


    class Meta:
        verbose_name_plural = 'Productos'
        ordering = ('-creado',)

    def get_absolute_url(self):
        return reverse('productos:producto_detalle', args=[self.slug])

    def __str__(self):
        return self.titulo
    
class Contacto(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='usuario')
   comentario = models.CharField(max_length=300)

   def __str__(self):
        return self.comentario
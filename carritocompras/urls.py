from django.urls import path
from . import views

app_name = 'carritocompras'

urlpatterns = [
    path('',views.carrito_suma, name="carrito_suma"),
    path('agregar/',views.carrito_agregar, name="carrito_agregar"),
    path('eliminar/',views.carrito_eliminar, name="carrito_eliminar"),
    path('modificar/',views.carrito_modificar, name="carrito_modificar"),


]

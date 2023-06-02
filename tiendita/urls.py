from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static


app_name = 'tiendita'


urlpatterns = [
    path('',views.listado,name="listado"),
    path('item/<slug:slug>/', views.productodetalle,name="producto_detalle"),
    path('search/<slug:categoria_slug>/', views.categoria_lista, name='categoria_lista'),
    path('agregarproducto/',views.agregarproducto,name="agregarproducto"),
    path('productos_pendientes/',views.productos_pendientes,name="productos_pendientes"),
    path('aprobar_producto/<int:pk>/',views.aprobar_producto,name="aprobar_producto"),
    path('rechazar_producto/<int:pk>/',views.rechazar_producto,name="rechazar_producto"),
    path('buscar_pendientes/', views.buscar_pendientes, name='buscar_pendientes'),
    path('mapa/', views.Vermapa, name="vermapa"),
    path('listadoventa/',views.listadoVenta, name="listadoventa"),

]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
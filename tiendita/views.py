from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Producto, Contacto
from carritocompras import carritocompras
from .forms import ProductoForm, ContactoForm, editItem
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from pedidos.models import Pedido
import googlemaps

# Create your views here.    

def listado(request):
    producto = Producto.producto.filter(aprobado = True)
    return render(request,"app/listado.html", {'producto': producto})

def productodetalle(request, slug):
    producto = get_object_or_404(Producto, slug=slug, en_stock=True)
    return render(request, 'app/detalle.html', {'producto': producto})

def categoria_lista(request, categoria_slug=None): 
    categoria = get_object_or_404(Categoria, slug = categoria_slug)
    productos = Producto.objects.filter(categoria = categoria)
    return render(request,'app/categorias.html', {'categoria': categoria, 'productos': productos})

def agregarproducto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.creado_por = request.user
            categoria_id = request.POST.get('categoria')
            # Asignar la categoría al producto
            producto.categoria_id = categoria_id
            producto.aprobado = False
            producto.save()
            messages.success(request, 'el producto se ha agregado, pero tiene que ser aprobado por el administrador')
            return redirect(to='tiendita:agregarproducto')
    else:
        form = ProductoForm()
    return render(request, 'app/agregarproducto.html', {'form': form})


@permission_required('app.delete_producto')
def productos_pendientes(request):
    productos = Producto.objects.filter(aprobado = False)
    return render(request,'app/productos_pendientes.html', {'productos': productos})

def aprobar_producto(request, pk):
    producto = get_object_or_404(Producto, pk = pk)
    producto.aprobado = True
    producto.save()
    return redirect('tiendita:productos_pendientes')

def rechazar_producto(request, pk):
    producto = get_object_or_404(Producto, pk = pk)
    producto.delete()
    return redirect('tiendita:productos_pendientes')


def buscar_pendientes(request):
    queryset = request.GET.get("buscar")#este es el nombre que sale el el buscador de la pagina productos pendientes.
    productos = Producto.objects.filter(aprobado=False)
    
    if queryset:
        productos = Producto.objects.filter(
            Q(titulo__icontains = queryset) |
            Q(descripcion__icontains = queryset)
        ).distinct()
    
    return render(request, 'app/productos_pendientes.html', {'productos': productos})


def Vermapa(request):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    direccion = 'Mall Plaza Norte'
    geocode_result = gmaps.geocode(direccion)

    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']

    context = {
        'direccion': direccion,
        'lat': lat,
        'lng': lng,
    }
    return render(request,'app/mapa.html', context)

@permission_required('app.view_pedido')
def listadoVenta(request):
    listar = Pedido.objects.all()
    return render(request,'app/listadoventa.html',{'listar': listar} )

def editarproducto(request, slug):
    producto = get_object_or_404(Producto, slug=slug, en_stock=True, creado_por = request.user)
    if request.method=='POST':
        form = editItem(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()

            return redirect('tiendita:producto_detalle', slug=producto.slug)
    
    else:
        form = editItem(instance=producto)
        
    return render(request, "app/formeditar.html", {
        'form': form,
        'title': 'Editar tu producto'
    })

def delete(request, slug):
    producto = get_object_or_404(Producto, slug=slug, en_stock=True, creado_por=request.user)
    producto.delete()
    return redirect('tiendita:listado')
def informacion(request):
    return render(request, 'app/informacion.html')


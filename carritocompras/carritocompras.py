from decimal import Decimal
from tiendita.models import Producto
from django.shortcuts import get_object_or_404



class Carrito():

    def __init__(self, request):
     
     """
    La aplicacion trabaja con sesiones, esta funcion inicializa el carro de compras del usuario
    que se llama carrito, si el usuario no tiene una sesion, se crea uno nuevo con la variable skey,
    para almacenarlo en la clase carrito.
    """
     
     self.session = request.session
     carrito = self.session.get('skey') #sesionkey
     if 'skey' not in request.session: #si la variable skey no existe se crea abajo con la variable carrito que va a gardar la skey en un diccionario
      carrito= self.session['skey'] = {}
     self.carrito = carrito

    def agregar(self, producto, qty):

      """
      funcion que permite agregar un producto al carrito de compras, con la variable carrito,
      el sistema busca el producto por su id y la cantidad que va a llevar el usuario para almacenar el producto
      al carrito.
      """
      
      producto_id = str(producto.id)

      if producto_id in self.carrito:
        self.carrito[producto_id]['qty'] = qty
      else:
        self.carrito[producto_id] = {'precio': str(producto.precio), 'qty' : qty, 'id_producto': str(producto.id)}
        
      self.guardar()

    def __iter__(self):

      """
      funcion que permite iterar un producto, se crean las variables para recorrer los datos que fueron creados
      anteriormente, la variable objects recorre la tabla 'Producto', y hace un filtrado de los productos mediante el id,
      la funcion carrito crea una copia del mismo para que el producto pueda ser manipulado y cambiar los datos sin errores.
      """

      producto_ids = self.carrito.keys()
      objects = Producto.objects.filter(id__in=producto_ids)
      carrito = self.carrito.copy()

      for producto in objects:
        carrito[str(producto.id)]['producto'] = producto

      for item in carrito.values():
        item['precio'] = Decimal(item['precio'])
        item['total_precio'] = item['precio'] * item['qty']
        yield item

    def __len__(self):

      """
      funcion que recorre la cantidad o largo del producto, si el usuario le agrega un producto
      este puede ser manipulado desde el frontend por el mismo usuario.
      """
      return sum(item['qty'] for item in self.carrito.values())
    
    def get_subtotal_precio(self):

      """
      funcion que devuelve el precio total de los productos.
      """
      return sum(Decimal(item['precio']) * item['qty'] for item in self.carrito.values())
    
    
    
    def get_total_precio(self):
      subtotal = sum(Decimal(item['precio']) * item['qty'] for item in self.carrito.values())

      if subtotal == 0:
        shipping = Decimal(0.00) #shipping es la compra 
      else:
        shipping = Decimal(3.500)
      
      total = subtotal + Decimal(shipping)
      return total  # le cambie el tipo de retorno, despues se lo vuelvo a cambiar

    def eliminar(self, producto):
      """
      funcion que permite eliminar un producto del carrito de compras, se crea la variable producto_id y el producto
      se pasa a un string.

      luego se valida si el producto esta agregado en el carrito de compras y elimina el producto del carro.
      """
      producto_id = str(producto)
      
      if producto_id in self.carrito:
        del self.carrito[producto_id]
        print(producto_id)
        self.guardar()

    def guardar(self):
      self.session.modified = True

    def modificar(self,producto, qty):

      """
      funcion que permite modificar el producto y la cantidad
      el sistema valida si el producto esta en el carrito para modificar la cantidad.
      """
      producto_id= str(producto)

      if producto_id in self.carrito:
        self.carrito[producto_id]['qty'] = qty

      self.guardar()

    def clear(self):
      #eliminar carrito de la sesion.
      del self.session['skey']
      self.guardar()

    def disminuirStock(self, producto):
      producto_id = producto
      qty = self.carrito[str(producto_id)]['qty']
      productos = get_object_or_404(Producto, id = int(producto_id))

      if productos.stock >= int(qty):
        productos.stock -= int(qty)
        productos.save()

        if productos.stock == 0:
          productos.delete()






from django.urls import path
from . import views

app_name = 'pago'

urlpatterns = [
    path('', views.carritoViews, name='carrito'),
    path('orderplaced/',views.order_placed, name= 'order_placed'),
    path('webhook/', views.stripe_webhook, name= 'stripe_webhook'),
]
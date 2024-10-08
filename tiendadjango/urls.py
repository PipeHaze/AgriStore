"""tiendadjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('tiendita.urls', namespace='tiendita')),
    path('carritocompras/',include('carritocompras.urls', namespace='carritocompras')),
    path('account/', include('account.urls', namespace='account')),
    path('pago/', include('pago.urls', namespace='pago')),
    path('pedidos/', include('pedidos.urls', namespace='pedidos')),
    path('inbox/', include('conversacion.urls')),
    

    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
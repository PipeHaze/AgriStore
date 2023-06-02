from .models import Producto, Categoria, Contacto
from django import forms

class ProductoForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all())

    class Meta:
        model = Producto
        fields = ['titulo', 'descripcion', 'imagen', 'precio', 'slug']

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['comentario']
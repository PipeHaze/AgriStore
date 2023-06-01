from .models import Producto, Categoria
from django import forms

class ProductoForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all())

    class Meta:
        model = Producto
        fields = ['titulo', 'descripcion', 'imagen', 'precio', 'slug']
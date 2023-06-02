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

class editItem(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('titulo', 'descripcion', 'precio', 'imagen','categoria')
        widgets={
            'titulo': forms.TextInput(attrs={
                'class':'form-control',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'precio': forms.TextInput(attrs={
                'class':'form-control',
                'type': 'number'
            }),
            'imagen': forms.FileInput(attrs={
                'class':'form-control',
                
            }),
            'categoria': forms.RadioSelect(attrs={
                'class': 'form-check-label'

            }),
                
        }    
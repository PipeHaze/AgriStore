from django import forms
from .models import UserBase
from django.contrib.auth.forms import(AuthenticationForm, PasswordResetForm, SetPasswordForm)


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Ingresa tu correo', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
        'class': 'form-control',
        'placeholder': 'Contraseña',
        'id': 'login-pwd',
        }
    ))

class RegistrationForm(forms.ModelForm):

    user_name = forms.CharField(
        label='Ingresa nombre de usuario', min_length=4,max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100,help_text='Required',error_messages={
        'required': 'Necesitas ingresar un email valido'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma contraseña', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email',)

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("El usuario ya existe")
        return user_name
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']: # comprueba si es que son distintos manda un mensaje de error
            raise forms.ValidationError('Contraseñas no coinciden')
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Ingresa otro correo, el que ingresaste ya esta registrado')
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Nombre de Usuario'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Ingresa Tu E-mail', 'name': 'email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirma contraseña'})

class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label='Correo registrado(no puede ser cambiado)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    first_name = forms.CharField(
        label='Usuario', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Nombre de usuario', 'id': 'form-lastname'}))

    class Meta:
        model = UserBase
        fields = ('email','first_name', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True

class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254,widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Hubo un error al encontrar tu correo electronico')
        return email
    
class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Nueva contraseña', widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Nueva contraseña', 'id': 'form-newpass'}))

    new_password2 = forms.CharField(
        label='Repite contraseña', widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Nueva contraseña', 'id': 'form-new-pass2'}))
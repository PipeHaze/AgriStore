from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserEditForm, UserAddressForm
from django.http import HttpResponse, HttpResponseRedirect
from .token import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .models import UserBase, Direccion
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from pedidos.views import pedido_usuarios
from django.urls import reverse

# Create your views here.

@login_required
def dashboard(request):
    pedido = pedido_usuarios(request) #trae los pedidos de los usuarios de esta vista creada
    return render(request,
                  'account/user/dashboard.html', {'pedido': pedido})

@login_required
def edit_details(request):
    """
    funcion que permite modificar el nombre de usuario en el dashboard
    """
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST) #formulario para editar usuario
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/user/edit_details.html', {'user_form': user_form})
                  

@login_required
def delete_user(request):
    """
    funcion que desactiva una cuenta, ya que en la base de datos el usuario no se borra
    """
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')

def account_register(request):   
    """
    al registrarse un usuario se validan los campos y el usuario no esta activo, supuestamente tiene que llegar un email, pero solo
    funciona con el BackEnd para la confirmacion del correo, cuando se abre el enlace la cuenta se activa.
    """
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            #configurar email
            current_site = get_current_site(request)
            subject = 'Activa tu cuenta'
            message = render_to_string('account/registration/account_activation_email.html',{
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message) # esto muestra el email simulado por el terminal de VSC
            return HttpResponse('Registro exitoso, activacion enviada,')
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})

def account_activate(request,uidb64, token):
    """Esta funcion muestra el mensaje para activar la cuenta cuando se registra un usuario"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)      
    except(TypeError):
        pass

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')

@login_required
def ver_direccion(request):
    direcciones = Direccion.objects.filter(usuario=request.user)
    return render(request, "account/user/direcciones.html", {"direcciones": direcciones})

@login_required
def agregar_direccion(request):
    if request.method == "POST":
        direccion_form = UserAddressForm(data=request.POST)
        if direccion_form.is_valid():
            direccion_form = direccion_form.save(commit=False)
            direccion_form.usuario = request.user
            direccion_form.save()
            return HttpResponseRedirect(reverse("account:direcciones"))
    else:
        direccion_form = UserAddressForm()
    return render(request, "account/user/editar_direccion.html", {"form": direccion_form})

@login_required
def editar_direccion(request, id):
    if request.method == "POST":
        direccion = Direccion.objects.get(pk=id, usuario = request.user)
        direccion_form = UserAddressForm(instance=direccion, data=request.POST)
        if direccion_form.is_valid():
            direccion_form.save()
            return HttpResponseRedirect(reverse("account:direcciones"))
        
    else:
        direccion = Direccion.objects.get(pk=id, usuario = request.user)
        direccion_form = UserAddressForm(instance=direccion)
    return render(request, "account/user/editar_direccion.html", {"form": direccion_form})

@login_required
def eliminar_direccion(request, id):
    direccion = Direccion.objects.get(pk=id, usuario=request.user).delete()
    return redirect("account:direcciones")

@login_required
def set_default(request, id):
    Direccion.objects.filter(usuario=request.user, default = True).update(default = False)
    Direccion.objects.filter(pk=id, usuario=request.user).update(default=True)
    return redirect("account:direcciones")

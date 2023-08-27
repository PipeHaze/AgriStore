from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserEditForm
from django.http import HttpResponse
from .token import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .models import UserBase
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from pedidos.views import pedido_usuarios

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
        user_form = UserEditForm(instance=request.user, data=request.POST)
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
            user.email_user(subject=subject, message=message)
            return HttpResponse('Registro exitoso, activacion enviada')
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


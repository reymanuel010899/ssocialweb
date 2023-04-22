import datetime
from django.shortcuts import render, redirect
from .models import User
from .form import UsuarioRegisterForm
from home.models import AmigoModels, PostModel
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import UserActivity
from .funciones import generar_codigo
from django.core.mail import send_mail
from django.conf import settings
from home.models import ChatModels
# Create your views here.



def registrar_usuario(request):
    form = UsuarioRegisterForm()
    codig = generar_codigo()
    if request.method == 'POST':
        username = request.POST.get('username')
        gmail = request.POST.get('gmail')
        perfil = request.FILES.get('perfil')
        if request.POST.get('password','') != request.POST.get('password2',''):
            return render(request, 'register.html', {"form":form, 'errores':"contraseñas incorrectas"} )
        try:
            user = User.objects.create_user(username, gmail, request.POST.get('password'), codigo=codig, avatar=perfil)
        except:
            return render(request, 'register.html', {"form":form, 'errores':"correo ya existe, intente con otro correo "} )
        redsocial = User.objects.get(id='1')
        mio , crd = AmigoModels.objects.get_or_create(user=user, añadidos=redsocial)
        obj , amigo = AmigoModels.objects.get_or_create(añadidos=user, user=redsocial)
        PostModel.objects.create(user=user, archivo=user.avatar)
        mensaje = "Bienvenido %s  espero que te la pases bien en kiptly"%(user.username)
        ChatModels.objects.create(user=redsocial, amigo=obj, mensaje=mensaje)
        asunto ='CODIGO DE VERIFICACION'
        messege = 'por favor agregar este codigo %s'%(codig)
        from_mail = settings.EMAIL_HOST_USER 
        send_mail(asunto, messege, from_mail, [gmail,])
        return redirect('users_app:verificar_codigo', username=user.username)
    return render(request, 'register.html', {"form":form} )




def iniciar_secion(request):
    if request.method == 'POST':
        gmail = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(gmail=gmail, password=password)
        if user:
            login(request, user)
            return redirect('inicio_app:inicio')
        else:
            return render(request, 'login.html', {'error':' este usuario no existe'} )
    return render(request, 'login.html')    



def logoutviews(request):
    if request.method == "GET":
        logout(request)
        return redirect('users_app:iniciar-secion')



@receiver(user_logged_in)
def user_login(sender, request, user, **kwargs):
    user_activity, created = UserActivity.objects.get_or_create(user=user)
    user_activity.last_activity = timezone.now()
    is_online = timezone.now() - user_activity.last_activity <= timezone.timedelta(minutes=5)
    if user.is_online != is_online:
        user.is_online = is_online
        user.save()
  

@receiver(user_logged_out)
def user_logout(sender, request, user, **kwargs):
    user_activity, created = UserActivity.objects.get_or_create(user=user)
    user_activity.last_activity = timezone.now()
    user.is_online = False
    user.save()
  


def verificar_codigo(request, username):
    if request.method=='POST':
        if username is not None:
            codigo = request.POST.get('codigo', '')
            if codigo != '':
                if User.objects.filter(username=username, codigo=codigo).exists():
                    user = User.objects.get(username=username)
                    login(request, user)
                    return redirect("inicio_app:inicio")
                return redirect('users_app:registrar')
            return render(request, 'codigo.html')
    return render(request, 'codigo.html')
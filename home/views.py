
from django.shortcuts import render, redirect
from .funciones import actualizarperfil,agregar_like_publicaciones,si_tu_like_existe, solicitud_enviada
from django.contrib.auth.decorators import login_required
from users.models import User
from .models import PostModel, LikeModels, SolisitudMOdel, ChatVistoModels,  AmigoModels, NotificacionesModels, ChatModels, ComentarModels, ConpartirModels, ComentarioLike
from users.models import InformacionPersonal
from django.db.models import Count,Q
from django.core.paginator import Paginator
from .context_processors import validar_amigo
from django.contrib.auth import logout, authenticate
from .forms import  userupdateavatar


@login_required(login_url='users_app:registrar')
def homeview(request):
    #activo = seciones_activas(request)
    usuario = User.objects.get(username=request.user.username)
    agregar_like_publicaciones(request)
    post_comentario = PostModel.objects.all().order_by("-created")
    existe = si_tu_like_existe(request,post_comentario)
    cant_amigos = AmigoModels.objects.filter(user=request.user).count()
    cant_like, cant_post = PostModel.objects.camtidades(usuario) 
    notificaciones = NotificacionesModels.objects.notificaciones(request.user).order_by('-created')[:5]
    uugerensias = AmigoModels.objects.sugerencias_amigos(request.user)
    sugerencia = User.objects.filter(id__in=uugerensias)[:5]
    usuarios_activos = AmigoModels.objects.filter(user=request.user,  añadidos__is_online=True)[:10]
    if request.method == 'POST':
        contenido = request.POST.get('status','')
        archivo = request.FILES.get('files','')
        if contenido != '' or archivo != '': 
            PostModel.objects.create(user=request.user, archivo=archivo,   descripcion=contenido)
    return render(request, 'index.html', {'posts':post_comentario,'notificaciones':notificaciones, "sugerencia":sugerencia,'usuarios_activos':usuarios_activos,'cantidad_conectados':usuarios_activos.count(),   })





@login_required(login_url='users_app:registrar')
def  perfil(request, username):
    user = request.user
    usuario = User.objects.get(username=username)
    cant_amigos = AmigoModels.objects.filter(user=usuario).count()
    cant_like, cant_post = PostModel.objects.camtidades(usuario) 
    amigo_o_no=validar_amigo(usuario, user)
    solicitud = solicitud_enviada(usuario, user)
    id_post = request.GET.get("like",'')
    if id_post != '':
        agregar_like_publicaciones(request)
    if request.method == "POST":
        contenido = request.POST.get('status','')
        archivo = request.FILES.get('files')
        if contenido and archivo:
            PostModel.objects.create(user=user, archivo=archivo,   descripcion=contenido)
        elif contenido or archivo:
            PostModel.objects.create(user=user, archivo=archivo, descripcion=contenido)
      
       
    status = PostModel.objects.filter(user__username=username).order_by('-created')
    ultimas_fotos = PostModel.objects.ultimas_fotos(usuario).order_by('-created')[:10]
    amigos_comun = AmigoModels.objects.obtener_amigos_en_comun(usuario, user )[:5]
    notificaciones= NotificacionesModels.objects.notificaciones(request.user)[:5]
    compatido =  ConpartirModels.objects.compartidos(usuario) 
    usuarios_activos = AmigoModels.objects.filter(user=request.user,  añadidos__is_online=True)[:10]
    return render(request , 'profile.html',{"estados":status, 'usuario':usuario, 'ultimas':ultimas_fotos,
                                             'comunes':amigos_comun, 'numero':len(amigos_comun),
                                               'notificaciones':notificaciones, 'amigo_o_no':amigo_o_no,
                                                 'cantidad_like':cant_like,'cantidad_post':cant_post,
                                                   'cantidad_amigos':cant_amigos, 'compartidos':compatido,
                                                     'usuarios_activos':usuarios_activos, 'cantidad_conectados':usuarios_activos.count(),
                                                      'enviada':solicitud})




@login_required(login_url='users_app:registrar')
def friend_views(request):
    solicitudes = SolisitudMOdel.objects.filter(solisitud=request.user)
    return render(request, "friends.html", {'usuarios':solicitudes})




def perfil_setting_views(request):
    user_perfile =  User.objects.get(username=request.user.username)
    form = userupdateavatar(instance=user_perfile,  initial={"avatar":None, "Currently":None})
    if request.method == "POST":
        nombres = request.POST.get('nombre','')
        if nombres != '':
            actualisado = actualizarperfil(request)
            if actualisado is not None:
                return redirect('inicio_app:perfil-about', username=actualisado.username)

        form = userupdateavatar(request.POST, request.FILES, instance=user_perfile, initial={'avatar':None})
        if form.is_valid():
            form.save()
            return redirect('inicio_app:inicio')
       
    return  render(request , 'perfil.html', {'form':form})



# @login_required(login_url='users_app:registrar')
# def  perfil_setting_views(request):
#     if request.method == 'GET':
#         return render(request , 'perfil.html')
#     else:        
       



@login_required(login_url='users_app:registrar')
def fotos_views(request, username):
    if request.method == "GET":
        usuario = User.objects.get(username=username)
        cant_amigos = AmigoModels.objects.filter(user=usuario).count()
        cant_like, cant_post = PostModel.objects.camtidades(usuario) 
        user=request.user
        amigo_o_no=validar_amigo(usuario, user)
        fotos =  PostModel.objects.filter(user__username=username).order_by("-created")
    return render(request, "photos.html",{'fotos':fotos,'usuarios':usuario, 'amigo_o_no':amigo_o_no, 'nun_post':cant_post, 'nun_like':cant_like, 'nun_amigo':cant_amigos})




@login_required(login_url='users_app:registrar')
def about_views(request, username):
    usuario = User.objects.get(username=username)
    cant_amigos = AmigoModels.objects.filter(user=usuario).count()
    cant_like, cant_post = PostModel.objects.camtidades(usuario) 
    user=request.user
    amigo_o_no=validar_amigo(usuario, user)
    amigos_comun = AmigoModels.objects.obtener_amigos_en_comun(usuario, user )[:5]
    ultimas_fotos = PostModel.objects.ultimas_fotos(usuario).order_by('-created')[:10]
    personal = InformacionPersonal.objects.filter(user__username=username).first()
    if personal:
        return render(request, "about.html", {'personal':personal,'persona':usuario, 'cantidad_amix':cant_amigos, 'cantidad_pots':cant_post,'cantidad_like':cant_like,  'amigo_o_no':amigo_o_no, 'usuario':usuario, 'fotos':ultimas_fotos, 'amigos':amigos_comun})
    return redirect('inicio_app:perfil-setting')


@login_required(login_url='users_app:registrar')
def buscar_contenido_views(request):
        agregar_like_publicaciones(request)
        post_comentario = PostModel.objects.all().order_by("-created")
        existe = si_tu_like_existe(request,post_comentario)
        notificaciones = NotificacionesModels.objects.notificaciones(request.user).order_by('-created')[:5]
        uugerensias = AmigoModels.objects.sugerencias_amigos(request.user)
        sugerencia = User.objects.filter(id__in=uugerensias)[:4]
        usuarios_activos = AmigoModels.objects.filter(user=request.user,  añadidos__is_online=True)[:10]
        if request.method == 'POST':
            contenido = request.POST.get('status','')
            archivo = request.FILES.get('files','')
            if contenido != '' or archivo != '':
                PostModel.objects.create(user=request.user, archivo=archivo,   descripcion=contenido)
                return redirect('inicio_app:inicio')
            return redirect('inicio_app:inicio')
        else:
            contenido = request.GET.get('buscar','')
            if contenido != '':
                resulatdo = User.objects.filtrar_contenido(contenido)
                publicaciones = PostModel.objects.filter(descripcion__icontains=contenido) 
                return render(request, 'contenido.html',{'encontrados':resulatdo,'publicaciones':publicaciones,'existe':existe, 'notificaciones':notificaciones, "sugerencia":sugerencia,'usuarios_activos':usuarios_activos,'cantidad_conectados':usuarios_activos.count()})
            return render(request, 'contenido.html',{'existe':existe, 'notificaciones':notificaciones, "sugerencia":sugerencia,'usuarios_activos':usuarios_activos,'cantidad_conectados':usuarios_activos.count()})




@login_required(login_url='users_app:registrar')
def agergar_like_status(request, pk):
    statud = PostModel.objects.get(id=pk)
    if statud:
       obj, cred = LikeModels.objects.get_or_create(post=statud, user=request.user)
       if cred:
            return redirect('inicio_app:profile', username=statud.user.username)
       else:
            obj.delete()
            return redirect('inicio_app:profile', username=statud.user.username)
   



@login_required(login_url='users_app:registrar')
def enviar_solicitud(request, username):
    if username is not None:
        usuario =  User.objects.get(username=username)
        obj, cred = SolisitudMOdel.objects.get_or_create(solisitud=usuario,  user=request.user)
        return redirect('inicio_app:profile', username=username)
    


@login_required(login_url='users_app:registrar')
def añadir_a_amigos(request, username):
    if username is not None:
        usuario =  User.objects.get(username=username)
        obj, cred=AmigoModels.objects.get_or_create(añadidos=usuario, user=request.user)
        if cred:
            AmigoModels.objects.create(user=usuario, añadidos=request.user)
            solicitud = SolisitudMOdel.objects.get(user__username=username)
            solicitud.delete()
            return redirect('inicio_app:friend')
        else:
            solicitud = SolisitudMOdel.objects.get(user__username=username)
            solicitud.delete()
            return redirect('inicio_app:friend')



@login_required(login_url='users_app:registrar')
def amigos_añadidos(request):
    amigos = AmigoModels.objects.filter(user=request.user)
    paginator = Paginator(amigos, 20)
    num_page = request.GET.get('page')
    page = paginator.get_page(num_page)
    return render(request, 'amigos_añadidos.html',{'page':page} )





@login_required(login_url='users_app:registrar')
def chats_usuarios(request, username):
    amix =User.objects.get(username=username)
    user=request.user
    amigo = AmigoModels.objects.get(user=user, añadidos=amix)
    amigo_2 = AmigoModels.objects.get(user=amix , añadidos=user)
    mensajes = ChatModels.objects.filter(Q(user=user)| Q(user=amix), Q(amigo=amigo) | Q(amigo=amigo_2)).order_by('-created')
    ultimos_mensaje_por_amigo=ChatModels.objects.ultimos_amigos(user)
    amigos_en_chat = AmigoModels.objects.filter(añadidos__id__in=ultimos_mensaje_por_amigo).distinct('añadidos__id',)
    if request.method == "GET":
        mensaje =  ChatModels.objects.filter(user=user, amigo=amigo).first()
        if mensaje:
            if  mensaje.amigo.añadidos.username != mensaje.user.username: 
                ChatVistoModels.objects.get_or_create(mensaje=mensaje, amigo=amigo,)

        return  render(request, 'chats.html',{"amigos":amigo,'messege':mensajes, 'amigos_chats':amigos_en_chat})
    else:
        buscar =  request.POST.get('buscar','')
        messege = request.POST.get('message-to-send','')
        if messege != '':
            ChatModels.objects.create(user=user, amigo=amigo, mensaje=messege)
            

        if buscar != '':
           filtrad =  AmigoModels.objects.filter(user=request.user, añadidos__username__icontains=buscar)
           if filtrad.exists():
               return  render(request, 'chats.html',{"amigos":amigo,'messege':mensajes, 'amigos_chats':filtrad})
           return redirect('inicio_app:buscar-contenido')
        return redirect('inicio_app:chat-usuario', username=username)
           
        
       


@login_required(login_url='users_app:registrar')
def ultimos_chats(request):
    user = request.user
    chat =  ChatModels.objects.filter(user=user).first()
    if chat:
        amigo = chat.amigo.añadidos
        return redirect('inicio_app:chat-usuario', username=amigo.username)
    return redirect('inicio_app:chat-usuario', username="kiptly")


@login_required(login_url='users_app:registrar')
def listar_notificaciones(request):
    if request.method == "GET":
        notificaciones = NotificacionesModels.objects.notificaciones(request.user).order_by('-created')[:15]
        return render(request, 'notificaciones.html', {"notificaciones":notificaciones, })



# @login_required(login_url='users_app:registrar')
# def cambiar_contraseña(request):
#     if request.method == "GET":
#         return render(request, 'ChanGe-Password.html')
#     else: 
#         vieja = request.POST.get('oldpassword','')
#         if vieja != '':
#             user = request.user
#             usuario = authenticate(gmail=request.user.gmail, password=vieja)
#             if usuario is not None:
#                 password1 = request.POST.get('password1','')
#                 password2 = request.POST.get('password2','')
#                 if  password1 and password2:
#                     if password1 == password2:
#                         user.set_password(password1)
#                         user.save()
#                         logout(request)
#                         return redirect('users_app:registrar')
#                     return render(request, 'ChanGe-Password.html',{'error':'introduzca las comtraseñas iguales'})
#             return render(request, 'ChanGe-Password.html',{'error':'introduzca la contraseña correcta'})      
#         return render(request, 'ChanGe-Password.html',{'error':'introduzca la contraseña vieja'})
    

def Settings_views(request):
    return render(request, 'Settings.html')





@login_required(login_url='users_app:registrar')
def feed_views(request, pk):
    post = PostModel.objects.catidaddes(pk)
    uugerensias = AmigoModels.objects.sugerencias_amigos(request.user)
    sugerencia = User.objects.filter(id__in=uugerensias)[:5]
    notificacion = NotificacionesModels.objects.notificaciones2(request.user)[:5]
    comen = ComentarModels.objects.filter(post=post).annotate(cantidad_comentario=Count('comentario_like_model')).order_by('-created')[:50]
    agregar_like_publicaciones(request)
    existe = si_tu_like_existe(request,post)
    like_com = request.GET.get('like_comentario','')
    if like_com != '':
        com = ComentarModels.objects.get(id=like_com)
        obj , crd = ComentarioLike.objects.get_or_create(comentario=com, user=request.user)
        if crd:
            return redirect('inicio_app:feed', pk=pk)
        else:
            obj.delete()
            return redirect('inicio_app:feed', pk=pk)
    
        
    if request.method == "POST":
        comentario = request.POST.get('comentario','')
        if comentario != '':
            ComentarModels.objects.create(user=request.user, post=post, mensaje=comentario)
     
    return render(request, 'feed.html',{"publicacion":post, 'comentarios':comen,'existe':existe,'sugerencia':sugerencia, 'notificaciones':notificacion})





@login_required(login_url='users_app:registrar')
def compartir_post(request, pk):
    amigos = AmigoModels.objects.filter(user=request.user)
    post = PostModel.objects.get(id=pk)
    pk_amigo = request.GET.get('agregar','')
    if pk_amigo != '':
        amigo = AmigoModels.objects.get(id=pk_amigo)
        ConpartirModels.objects.create(user=request.user, post=post, amigo=amigo)
        return redirect("inicio_app:profile", username=amigo.añadidos.username)
    return render(request, 'conpartir.html', {'amigos':amigos, 'post':post})




@login_required(login_url='users_app:registrar')
def sugerencias_amigos_views(request):
    if request.method == "GET":
        uugerensias = AmigoModels.objects.sugerencias_amigos(request.user)
        sugerencia = User.objects.filter(id__in=uugerensias)[:20]
        return render(request, 'sugerencia-amigo.html', {"sugerencias":sugerencia})
    





def comentar_post(request, pk):
    if request.method == 'POST':
        post = PostModel.objects.get(pk=pk)
        if post:
            comentar = request.POST.get('comentar','')
            if comentar != '':
                ComentarModels.objects.create(user=request.user,post=post, mensaje=comentar)
                return redirect('inicio_app:profile', username=post.user.username)
            return redirect('inicio_app:profile', username=post.user.username)
        


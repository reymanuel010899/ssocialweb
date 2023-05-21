from PIL import Image
from django.db import models
from users.models import User
from .manayers import PostManayes, AmigosManayer,ChatsManayers, NotificacionesManayer, CompartidosManayer
from django.db.models.signals import post_save
# from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class SolisitudMOdel(models.Model):
    user = models.ForeignKey(User, related_name="solicitud_reverse", on_delete=models.CASCADE)
    solisitud = models.ForeignKey(User, related_name="user_solicitud_reverse", on_delete=models.CASCADE)
    Created = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        verbose_name = "solisitud"

    def __str__(self) -> str:
        return self.user.username
    

class AmigoModels(models.Model):
    user = models.ForeignKey(User, related_name="user_añadidos" , on_delete=models.CASCADE)
    añadidos = models.ForeignKey(User, related_name="añadidos_user", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    objects = AmigosManayer()
    class Meta:
        verbose_name = "amigos"
       
       

    def __str__(self) -> str:
        return self.añadidos.username
    

class PostModel(models.Model):
    user = models.ForeignKey(User, related_name="post_user_reverse",  on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='post/archivo')
    video = models.FileField(upload_to='post/videos', null=True,  blank=True)
    images=models.ImageField(upload_to='post/imagenes', null=True, blank=True)
    descripcion = models.TextField(verbose_name="descripcion", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = PostManayes()
    class Meta:
        verbose_name = "publicaciones"


    def __str__(self) -> str:
        return self.user.username
    
class LikeModels(models.Model):
    user = models.ForeignKey(User, related_name="like_user_reverse", on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, related_name="like_post_reverse", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "me gusta"


    def __str__(self) -> str:
        return self.user.username
    
class ComentarModels(models.Model):
    user = models.ForeignKey(User, related_name="comentario_user_reverse", on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, related_name='comentario_post_reverse', on_delete=models.CASCADE)
    mensaje = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "comentarios"


    def __str__(self) -> str:
        return self.user.username
    


class ComentarioLike(models.Model):
    user = models.ForeignKey(User, related_name="comentario_user_like_reverse", on_delete=models.CASCADE)
    comentario = models.ForeignKey(ComentarModels, related_name="comentario_like_model", on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username
    
class ConpartirModels(models.Model):
    user = models.ForeignKey(User, related_name="conpatir_user_reverse", on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, related_name="concartir_post_riverse", on_delete=models.CASCADE)
    amigo = models.ForeignKey(AmigoModels , related_name="conpartir_amigos_reverce", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    objects =  CompartidosManayer()

    class Meta:
        verbose_name = "conpartidos"

    def __str__(self) -> str:
        return self.user.username
    


class NotificacionesModels(models.Model):
    user = models.ForeignKey(User, related_name="notificaciones_reverce", on_delete=models.CASCADE)
    solicitud = models.ForeignKey(SolisitudMOdel, blank=True, null=True, related_name="solicitud_notificaciones_reverce", on_delete=models.CASCADE)
    amigo = models.ForeignKey(AmigoModels, blank=True, null=True, related_name="notificacion_amigo_reverse", on_delete=models.CASCADE)
    usuarios = models.ForeignKey(User, related_name="usuarios_reverce", blank=True, null=True, on_delete=models.CASCADE)
    comentarios = models.ForeignKey(ComentarModels, blank=True, null=True, related_name="Comentariosreverse", on_delete=models.CASCADE)
    like = models.ForeignKey(LikeModels, related_name="like_noti", blank=True, null=True, on_delete=models.CASCADE)
    solicitud_enviada = models.ForeignKey(AmigoModels, blank=True, null=True, related_name="solicitud_enviada", on_delete=models.CASCADE)
    mensaje = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    objects = NotificacionesManayer()
    class Meta:
        verbose_name = "motificacione"
        verbose_name_plural = "notificaciones"

    def __str__(self) -> str:
        return self.mensaje
    


class ChatModels(models.Model):
    user = models.ForeignKey(User, related_name="usuario_chats_reverse", on_delete=models.CASCADE)
    amigo = models.ForeignKey(AmigoModels, related_name="amigo_chats_reverse", on_delete=models.CASCADE)
    mensaje = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    objects = ChatsManayers()
    
    class Meta:
        verbose_name = "chat "
        verbose_name_plural = "chats"
        ordering = ['-created', 'amigo']
       

    def __str__(self) -> str:
        return  self.mensaje


class ChatVistoModels(models.Model):
    amigo = models.ForeignKey(AmigoModels, related_name="Amigochatview", on_delete=models.CASCADE)
    mensaje = models.ForeignKey(ChatModels, blank=True, related_name="chatvistamodel", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.amigo.añadidos.username


# def optimizar_imagen(sender, instance, **kwards):
#     if instance.archivo:
#         archivo = Image.open(instance.archivo.path)
#         archivo.save(instance.archivo.path, quality=30, optimize=True)
   
# post_save.connect(optimizar_imagen, sender=PostModel)   




def ha_acectado_la_solicitud(instance, sender, *args, **kwargs):
    id_añadido = instance.user.id
    añadido=User.objects.get(id=id_añadido)
    amigo = AmigoModels.objects.get(user=instance.user, añadidos=instance.añadidos)
    username = str(instance.user.username).upper()
    messege = "EN hora buena ya puedes Chactear con  %s"%(username)
    NotificacionesModels.objects.create(user=añadido,solicitud_enviada=amigo, mensaje=messege)
post_save.connect(ha_acectado_la_solicitud, sender=AmigoModels)




def notificar_resivo_messeges(instance, sender, *args, **kwargs):
    id_mensage = instance.id
    user=instance.user
    if id_mensage is not None:
        user=instance.amigo.añadidos
        amigo = instance.user
        amigo = AmigoModels.objects.filter(user=user,  añadidos=amigo).first()
        if amigo:
            username = str(instance.user.username).upper()
            mensage = "%s Te ha mandado un mensage '%s' "%( username , instance.mensaje)
            NotificacionesModels.objects.create(user=user,  amigo=amigo ,mensaje=mensage)
post_save.connect(notificar_resivo_messeges, sender=ChatModels)




def añadir_notififaciones(instance, sender, *args, **kwargs):
    solisitud = instance.solisitud.id
    user = instance.user
    user_solicitud = instance.solisitud
    if user_solicitud is not None:
        solicitud =  SolisitudMOdel.objects.filter(user=instance.user,  solisitud__id=solisitud).first()
        username = str(instance.user.username).upper()
        mensaje = "%s te ha mandado una solicitud de amistad !"%(username)
        user = User.objects.get(id=solisitud)
        NotificacionesModels.objects.create(user=user, solicitud=solicitud, mensaje=mensaje)
post_save.connect( añadir_notififaciones, sender=SolisitudMOdel)



def notificar_like(instance, sender, *args, **kwargs):
    print(instance)
    id_user = instance.user.id
    if id_user is not None:
        user_post_id = instance.post.user.id
        user_like = User.objects.get(id=user_post_id)
        user_dio_like = LikeModels.objects.filter(user=instance.user, post=instance.post).first()
        username = str(instance.user.username).upper()
        menssage = "%s reaciono a tu foto  '%s' !"%(username, instance.post.descripcion)
        NotificacionesModels.objects.create(user=user_like, like=user_dio_like, mensaje=menssage)
post_save.connect(notificar_like, sender=LikeModels)



def notificar_comentario(instance, sender, *args, **kwargs):
    persona_cometo = instance.user
    if persona_cometo is not None:
        username = str(persona_cometo.username).upper()
        post_description = instance.mensaje
        menssage = "%s Comento tu foto '%s' "%(username, post_description)
        comentario = ComentarModels.objects.filter(user=instance.user, post=instance.post).first()
        user=User.objects.get(username=instance.post.user.username)
        NotificacionesModels.objects.create(user=user, comentarios=comentario, mensaje=menssage)
post_save.connect(notificar_comentario, sender=ComentarModels)



def convertir_video_o_imagenes(instance, sender, *args, **kwargs):
    archivo = instance.archivo
    archivo = str(archivo).lower()
    formato = ''
    if archivo is not None:
        formato = archivo[-4:]
        if formato == '.jpg' or formato == '.png' or formato == 'jpeg' or formato == 'webp':
            PostModel.objects.filter(id=instance.id).update(images=archivo)
        elif formato == '.mp3' or formato == '.mp4':
            PostModel.objects.filter(id=instance.id).update(video=archivo)
post_save.connect(convertir_video_o_imagenes, sender=PostModel)
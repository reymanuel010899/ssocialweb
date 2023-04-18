from django.db import models
from django.db.models import Count, Sum, F,Q


class StatusManayers(models.Manager):
    def contar_like (self):
        pass

class PostManayes(models.Manager):
    def ultimas_fotos(self, ususario):
        return self.filter(user__id=ususario.id).order_by('created')


    def camtidades(self, usuario):
        like = self.filter(user=usuario).values('id').annotate(cantid = Count('like_post_reverse__id')) 
        lista = list()
        [lista.append(numero['cantid']) for numero in like ]
        post = self.filter(user=usuario).count()
        return sum(lista), post
    
    
    def catidad_de_comentario(self):
        cantida =  self.all()
        return cantida
    
    def catidaddes(self, pk):
        return self.filter(pk=pk).annotate(cantidad=Count('comentario_post_reverse__id'), cantidad_compatido=Count('concartir_post_riverse__id'), cantidad_like=Count('like_post_reverse__id')).first()
        
    



class ChatsManayers(models.Manager):
    def ultimos_amigos(self, user):
        mensage = self.filter(user=user)
        lista=set()
        for id_amix in mensage:
            lista.add(id_amix.amigo.añadidos.id)
        return list(lista)





class AmigosManayer(models.Manager):
    def obtener_amigos_en_comun(self, amigo_id, user_id):
        resultado =  self.filter(user=user_id)
        amigo = self.filter(user=amigo_id)
        id_amix_user = set()
        id_amix = set()
        for user in resultado:
            id_amix_user.add(user.añadidos.id)
        for amix in amigo:
            id_amix.add(amix.añadidos.id)
        comunes_id = id_amix_user.intersection(id_amix)
        amigo_comun = self.filter(añadidos__id__in=list(comunes_id)).distinct('añadidos_id')
        return  amigo_comun
    

    def listar_amigos_en_el_chat(self, ultimos):
        return self.filter(id__in=ultimos)
    


    def sugerencias_amigos(self, user):
        amigos = self.filter(user=user)
        id_amix = set()
        for amix in amigos:
            id_amix.add(amix.añadidos.id)
        sugerencia = self.filter(user__id__in = list(id_amix)).distinct().exclude(user=user)
        id_sug = set()
        for sug in sugerencia:
            id_sug.add(sug.añadidos.id)
        id_sug = id_sug.difference(id_amix)
        # sugerencia = self.filter(user__id__in=list(id_sug))
        return list(id_sug)


class publicacionManayer(models.Manager):
    def contar_like(self, user):
        like = self.filter(seguidor=user).values('publicaciones_like_reverse__id').annotate(cantid = Count('publicaciones_like_reverse__id')) 
        lista = list()
        [lista.append(numero['cantid']) for numero in like  ]
        return like
    

class NotificacionesManayer(models.Manager):
    def notificaciones(self, user):
        noti = self.filter(user=user).order_by('-created')
        #
        return  noti
    
    def notificaciones2(self, user):
        otro = self.filter(solicitud_enviada__añadidos=user).order_by('-created')
        return otro
    
class CompartidosManayer(models.Manager):
    def compartidos(self, usuarios):
        conpartidos = self.filter(amigo__añadidos=usuarios).annotate(nun_like=Count('post__like_post_reverse__post'), nun_comentario=Count('post__comentario_post_reverse'), nun_conpartido=Count('post__concartir_post_riverse') ) .order_by('-created')
        for a in conpartidos:
            print(a, a.nun_comentario)
        return conpartidos
    
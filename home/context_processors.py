from .models import AmigoModels, SolisitudMOdel, PostModel
from django.contrib.auth.decorators import login_required
from django.db.models  import Sum, Count
def validar_amigo(usuario, user):
    if AmigoModels.objects.filter(user=user, añadidos=usuario).exists():
        return True
    else:
        return False 
    


def amigos_context(request):
    
    if request.user.is_authenticated:
        post = PostModel.objects.filter(user=request.user).count()
        cantidad = SolisitudMOdel.objects.filter(solisitud=request.user).count()
        amigos = AmigoModels.objects.filter(user=request.user).count()
        # cant_like, cant_post = PostModel.objects.camtidades(request.user) 
        like = PostModel.objects.filter(user=request.user).values('like_post_reverse__id').annotate(cantid = Count('like_post_reverse__id')) 
        lista = list()
        [lista.append(numero['cantid']) for numero in like  ]
        
        return {
            'cantidad_post':post,
            'cantidad_solicitud':cantidad,
            'cantidad_like':sum(lista),
            'cantidad_amigo':amigos
        
            
        }
    else:
          return {
            
        }
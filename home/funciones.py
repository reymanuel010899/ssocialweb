import datetime
from users.models import User
from django.shortcuts import redirect
from users.models import User, InformacionPersonal
from .models import LikeModels, PostModel, SolisitudMOdel


def actualizarperfil(request):
    nombres = request.POST.get('nombre','')
    apellido = request.POST.get('apellido','')
    redsocia = request.POST.get('webside','')
    cumpleaño = request.POST.get('cumpleaño','')
    telefono = request.POST.get('telefono','')
    pais = request.POST.get('pais','')
    municipio =  request.POST.get('municipio','')
    provincia = request.POST.get('provincia','')
    otro = request.POST.get('otro','')
    femnino =  request.POST.get('femenino','')
    masculino =  request.POST.get('masculino','')
    casado = request.POST.get('casado','')
    soltero = request.POST.get("soltero","")
    descripcion = request.POST.get('descripcion','')

    upd, crd=User.objects.update_or_create( 
            gmail=request.user.gmail,
            defaults={
                'nombre':nombres,
                'apellido':apellido,
                'genero':masculino if masculino != '' else femnino,
                'ubicacion':request.user.ubicacion,
            }
         
                    )
    
    cumpleañ = datetime.datetime.strptime(cumpleaño, "%Y-%m-%d").date()

    updat, cread  = InformacionPersonal.objects.update_or_create(
        user=request.user,
        defaults={
        "webside":redsocia,
        "birthday":cumpleañ,
        "estado":provincia,
        "pais":pais,
        "status":casado if casado != '' else soltero,
        "telefono":telefono,
        "descripcion":descripcion

        }
     )
    if cread:
        act = updat
    else:
        act = updat
    return act.user


def agregar_like_publicaciones(request):
    pk = request.GET.get('like','')
    if pk != '':
        statud = PostModel.objects.get(id=pk)
        if statud:
            obj, cred = LikeModels.objects.get_or_create(post=statud, user=request.user)
            if cred:
                    return redirect('inicio_app:inicio', )
            else:
                obj.delete()
                return redirect('inicio_app:inicio')
    
    return redirect('inicio_app:inicio')



def si_tu_like_existe(request, post):
    user= request.user
    pk = request.GET.get('like','' )
    if pk != '':
        post = PostModel.objects.get(id=pk)
        if LikeModels.objects.filter(user=user, post=post).exists():
            return True
        else:
            return False
    return redirect('inicio_app:inicio')
    


def solicitud_enviada(usuario, user):
    if usuario is not None:
        if SolisitudMOdel.objects.filter(user=user, solisitud=usuario).exists():
           return True
        return False

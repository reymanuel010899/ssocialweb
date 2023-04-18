from django.contrib import admin
from .models import (SolisitudMOdel, AmigoModels, ChatModels, PostModel, LikeModels, ComentarModels , ConpartirModels,
                     NotificacionesModels,ComentarioLike,
                     ChatVistoModels   )

# Register your models here.
admin.site.register(SolisitudMOdel)
admin.site.register(AmigoModels)
admin.site.register(PostModel)
admin.site.register(LikeModels)
admin.site.register(ComentarModels)
admin.site.register(ConpartirModels)
admin.site.register(NotificacionesModels)
admin.site.register(ChatModels)
admin.site.register(ComentarioLike)
admin.site.register(ChatVistoModels)
from django.urls import path
from . import views

app_name = 'inicio_app'


urlpatterns = [
    path('', views.homeview, name='inicio' ),
    path('perfil/<username>/', views.perfil, name='profile'),
    path('solicitudes/', views.friend_views, name="friend"),
    path('perfil-setting/', views.perfil_setting_views, name="perfil-setting"),
    path('perfil-photos/<username>/', views.fotos_views, name="perfil-photos"),
    path('perfil-about/<username>/', views.about_views, name="perfil-about"),
    path('buscar-contenido/', views.buscar_contenido_views, name="buscar-contenido"),
    path('agreagr-like-status/<pk>/', views.agergar_like_status, name="agregar-like"),
    path('enviar-solicitud/<username>/', views.enviar_solicitud, name="enviar-solicitud"),
    path('agregar-amigos/<username>/', views.añadir_a_amigos, name="agregar-amigos"),
    path('friend-añadidos/', views.amigos_añadidos, name="friend-añadidos"),
    path('chat-usuario/<username>/', views.chats_usuarios, name="chat-usuario"),
    path("ultimo-chat/", views.ultimos_chats, name="ultimo-chat"),
    path('listar-notificaciones/', views.listar_notificaciones, name="listar-notificaciones"),
    path("Settings/", views.Settings_views, name="Settings"),
    path("feed/<pk>/", views.feed_views, name="feed"),
    path("compartir-post/<pk>/", views.compartir_post, name="compartir-post"),
    path('sugerencia-amigo/', views.sugerencias_amigos_views, name="sugerencia-amigo"),
    path('comentar-post-profile/<pk>/',  views.comentar_post, name="comentar-post-profile" ),
    path('eliminar-post/<pk>/', views.eliminar_post, name="eliminar-post"),
    path('eliminar-conpartido/<pk>/', views.eliminar_conpartidos, name="eliminar-conpartido")
    # path('cambiar-perfil/', views.cambiar_perfil, name="cambiar-perfil")
    #path('cambiar-contraseña/', views.cambiar_contraseña, name="cambiar-contraseña"),
    

]

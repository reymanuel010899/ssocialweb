from django.urls import path
from . import views
app_name = 'users_app'

urlpatterns = [
    path('registrar/', views.registrar_usuario, name='registrar'),
    path('', views.iniciar_secion, name='iniciar-secion'),
    path('logout/', views.logoutviews, name="logout"),
    path('verificar-codigo/<username>', views.verificar_codigo, name="verificar_codigo")
]

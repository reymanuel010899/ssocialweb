from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manayers import usermaneyer
from django.utils import timezone
from django.conf import settings




class UserActivity(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_activity = models.DateTimeField(default=timezone.now)
    last_profile_update = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.user.username




class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    gmail = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    genero = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='avatar/archivos')
    ubicacion = models.CharField(max_length=70)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    codigo = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now_add=True)
    is_online = models.BooleanField(default=False)
    objects = usermaneyer()
    USERNAME_FIELD = 'gmail'
    REQUIRED_FIELDS = ['username',]
    

    def update_online_status(self, user):
        is_online = timezone.now() - user.last_activity <= timezone.timedelta(minutes=5)
        if self.is_online != is_online:
            self.is_online = is_online
            self.save(update_fields=['is_online'])
        return is_online
    
    
  
    def __str__(self):
        return str(self.id)+ '-'+ self.username


class InformacionPersonal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    webside = models.URLField(verbose_name="redes sociales", blank=True)
    birthday = models.DateField(verbose_name="fecha de cumpleaño", blank=True )
    estado = models.CharField(max_length=50, blank=True)
    pais = models.CharField(max_length=50, blank=True)
    status = models.CharField(verbose_name="estado civil", max_length=20, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    descripcion = models.TextField(verbose_name="describete", blank=True)


    def __str__(self) -> str:
        return self.user.username
    




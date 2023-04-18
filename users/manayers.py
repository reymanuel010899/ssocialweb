from django.db import models
from django.db.models import Q
from django.contrib.auth.models import BaseUserManager
from django.contrib.postgres.search import TrigramSimilarity
class usermaneyer(BaseUserManager):
    def _create_user(self, username, gmail,  password, is_staff, is_superuser,  **extra_fields):
        user =  self.model(
            username=username,
            gmail=gmail,
            is_staff=is_staff,
            is_superuser=is_superuser,
             **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, gmail,   password,  **extra_fields):
        return self._create_user(username, gmail,password,False,False, **extra_fields)    

    def create_superuser(self, username, gmail, password , **extra_fields ):
        return self._create_user(username, gmail,  password, True, True, **extra_fields)
    
    
    def filtrar_contenido(self, contenido):
        return self.filter(Q(username__icontains=contenido)|Q(post_user_reverse__descripcion__icontains=contenido)) .distinct()
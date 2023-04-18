from django.contrib import admin
from .models import User, InformacionPersonal, UserActivity



admin.site.register(User)
admin.site.register(InformacionPersonal)
admin.site.register(UserActivity)
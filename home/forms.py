from django.forms import ModelForm
from django import forms
from users.models import User
from django.forms import ClearableFileInput

class  userupdateavatar(ModelForm):
    class Meta:
        model=User
        fields = ('avatar',)
       
    
    
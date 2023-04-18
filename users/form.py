from .models import User

from django import forms



class UsuarioRegisterForm(forms.Form):
    username = forms.ChoiceField(widget=forms.TextInput(attrs={"class":"input100","placeholder":"username"}))
    gmail =  forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class":"input100","placeholder":"gmail"}) )
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"input100","placeholder":"password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"input100","placeholder":"repeat password"}))
    
 
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserModel


class CursoFormulario(forms.Form):
    curso = forms.CharField()
    camada = forms.IntegerField()


class ProfesorFormulario(forms.Form):
    nombre = forms.CharField()
    apellido = forms.CharField()
    email = forms.EmailField()
    profesion = forms.CharField()


class UserCreationFormCustom(UserCreationForm):
    username = forms.TextInput()
    email = forms.EmailField()
    password1=forms.CharField(label="contraseña",widget=forms.PasswordInput)
    password2=forms.CharField(label="Repetir contraseña",widget=forms.PasswordInput)
    class Meta:
        model = UserModel
        fields = ["username","email","password1","password2"]

        #Mensaje de ayuda
        help_texts = {k:""for k in fields}
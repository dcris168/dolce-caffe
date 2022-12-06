from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

class CustomUsuarioCreateForm(UserCreationForm):

    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'cpf','estado', 'cidade', 'rua', 'numero', 'cep', 'celular', 'dataNascimento', 'username', 'email')
        labels = {'username': 'Username/E-mail'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
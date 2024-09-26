from django import forms
from .models import CustomUser, CustomUserManager

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['tipo_id', 'numero_identificacion', 'Nombres', 'Apellidos']
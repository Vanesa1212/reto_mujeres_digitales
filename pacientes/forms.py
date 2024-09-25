from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['tipo_id', 'numero_identificacion', 'Nombres', 'Apellidos']
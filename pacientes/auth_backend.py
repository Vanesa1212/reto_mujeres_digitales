from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, tipo_documento=None, numero_documento=None, fecha_nacimiento=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(tipo_id=tipo_documento, numero_identificacion=numero_documento, fecha_nacimiento=fecha_nacimiento)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

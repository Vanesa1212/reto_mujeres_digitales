from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class Usuario(models.Model):
    TIPO_ID = (
        ('CC', 'Cédula de ciudadanía'),
        ('TI', 'Tarjeta de identidad'),
        ('CE', 'Cédula de extranjería'),
        ('RC', 'Registro civil'),
        ('PA', 'Pasaporte'),
        ('AS', 'Adulto sin identificación'),
        ('MS', 'Menor sin identificación'),
        ('NU', 'Número único de identificación'),
        ('NV', 'Certificado de nacido vivo'),
        ('SC', 'Salvoconducto'),
        ('NIT', 'Nit'),
        ('CD', 'Carnet diplomático'),
        ('PE', 'Permiso especial de permanencia'),
        ('RE', 'Residente especial para la paz'),
        ('PT', 'Permiso por protección temporal'),
        ('DE', 'Documento extranjero'),
    )

    tipo_id = models.CharField(max_length=100, choices=TIPO_ID, blank=False)
    numero_identificacion = models.CharField(
        max_length=20,
        blank=False,
        validators=[RegexValidator(regex=r'^\d+$', message='El número de identificación solo puede contener números.')]
    )
    nombres = models.CharField(max_length=100, blank=False)
    apellidos = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=255, blank=False, unique=True)
    telefono = models.CharField(max_length=15, blank=False)
    fecha_nacimiento = models.DateField()

    USERNAME_FIELD = 'numero_identificacion'
    REQUIRED_FIELDS = ['tipo_id', 'nombres', 'apellidos', 'email', 'telefono', 'fecha_nacimiento']

    def save(self, *args, **kwargs):
        # Verifica si el usuario ya existe antes de crearlo
        User = get_user_model()  # Obtener el modelo de usuario configurado (Usuario)
        if not User.objects.filter(numero_identificacion=self.numero_identificacion).exists():
            # Crear automáticamente un usuario con los datos ingresados por el administrador
            User.objects.create_user(
                tipo_id=self.tipo_id,
                numero_identificacion=self.numero_identificacion,
                fecha_nacimiento=self.fecha_nacimiento,
                nombres=self.nombres,
                apellidos=self.apellidos,
                email=self.email,
                telefono=self.telefono
            )
        super(Usuario, self).save(*args, **kwargs)  # Llama al método save del modelo base para guardar el objeto

    def __str__(self):
        return f'{self.nombres} {self.apellidos} - {self.numero_identificacion}'


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, tipo_documento=None, numero_documento=None, fecha_nacimiento=None, **kwargs):
        try:
            user = Usuario.objects.get(tipo_id=tipo_documento, numero_identificacion=numero_documento, fecha_nacimiento=fecha_nacimiento)
            return user
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUserManager(BaseUserManager):
    def create_user(self, numero_identificacion, tipo_id, nombres, apellidos, email, telefono, fecha_nacimiento):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(
            numero_identificacion=numero_identificacion,
            tipo_id=tipo_id,
            nombres=nombres,
            apellidos=apellidos,
            email=email,
            telefono=telefono,
            fecha_nacimiento=fecha_nacimiento,
        )
        user.save(using=self._db)  # Guardar el usuario sin contraseña
        return user

    def create_superuser(self, numero_identificacion, tipo_id, nombres, apellidos, email, telefono, fecha_nacimiento):
        user = self.create_user(
            numero_identificacion,
            tipo_id,
            nombres,
            apellidos,
            email,
            telefono,
            fecha_nacimiento,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser, PermissionsMixin):
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
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    numero_identificacion = models.CharField(max_length=20, unique=True)
    tipo_id = models.CharField(max_length=100, choices=TIPO_ID)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    telefono = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField()

    objects = CustomUserManager()

    USERNAME_FIELD = 'numero_identificacion'
    REQUIRED_FIELDS = ['tipo_id', 'nombres', 'apellidos', 'email', 'telefono', 'fecha_nacimiento']

    def __str__(self):
        return f'{self.nombres} {self.apellidos} - {self.numero_identificacion}'

@receiver(post_save, sender=CustomUser)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        instance.save()  # Guarda el usuario creado

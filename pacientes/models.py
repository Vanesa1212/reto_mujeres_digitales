from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, numero_identificacion, tipo_id, nombres, apellidos, email, telefono, fecha_nacimiento, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        if not numero_identificacion:
            raise ValueError('El usuario debe tener un número de identificación')

        user = self.model(
            email=self.normalize_email(email),
            numero_identificacion=numero_identificacion,
            tipo_id=tipo_id,
            nombres=nombres,
            apellidos=apellidos,
            telefono=telefono,
            fecha_nacimiento=fecha_nacimiento
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, numero_identificacion, tipo_id, nombres, apellidos, email, telefono, fecha_nacimiento, password):
        user = self.create_user(
            numero_identificacion=numero_identificacion,
            tipo_id=tipo_id,
            nombres=nombres,
            apellidos=apellidos,
            email=email,
            telefono=telefono,
            fecha_nacimiento=fecha_nacimiento,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    TIPO_ID_CHOICES = [
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
    ]

    numero_identificacion = models.CharField(max_length=20, unique=True)
    tipo_id = models.CharField(max_length=100, choices=TIPO_ID_CHOICES)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    telefono = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_set',
        related_query_name='user',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_set',
        related_query_name='user',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'numero_identificacion'
    REQUIRED_FIELDS = ['tipo_id', 'nombres', 'apellidos', 'email', 'telefono', 'fecha_nacimiento']

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.numero_identificacion}"

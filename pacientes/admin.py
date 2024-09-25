from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from .models import CustomUser

# Registramos el modelo Usuario
admin.site.register(CustomUser)

# Desregistramos User solo si es necesario
# admin.site.unregister(User)  # Solo si necesitas personalizar el UserAdmin

# No registramos Group nuevamente, ya que ya está registrado por Django
# admin.site.unregister(Group)  # Esto es opcional, puedes dejarlo registrado

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import CustomUser

admin.site.register(CustomUser)

class CustomUserAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass


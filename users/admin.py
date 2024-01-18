from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = ("Profile", {"fields": ("email", "username", "mobile"),}),

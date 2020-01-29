from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import BaseUser


# Register your models here.
class UserAdmin(BaseUserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )

admin.site.register(BaseUser, UserAdmin)

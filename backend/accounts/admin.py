from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import  User, MobileToken


@admin.register(User)
class UserAdmin(DefaultUserAdmin):

    list_display = ('username',
                    'email',
                    'role',
                    'is_staff',
                    'is_active',
                    'mobile',
                    'verified_mobile',
                    'profile_pic')


@admin.register(MobileToken)
class MobileTokenAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'token',
        'is_expired',
        'created_at',
        'updated_at'
    )
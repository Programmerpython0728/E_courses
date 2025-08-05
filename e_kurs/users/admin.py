from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Maxsus User modelini admin panelda ro'yxatdan o'tkazish.
    Bu class foydalanuvchilarni admin panel orqali boshqarish uchun qulay interfeys yaratadi.
    """

    # Ro'yxatdagi ko'rsatiladigan maydonlar
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')

    # Ro'yxatdagi filtlar
    list_filter = ('role', 'is_staff', 'is_active')

    # Qidirish uchun maydonlar
    search_fields = ('email', 'first_name', 'last_name')

    # Tartiblash uchun maydon
    ordering = ('email',)

    # Admin panelda maydonlarni guruhlash
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Shaxsiy ma\'lumotlar',
         {'fields': ('first_name', 'last_name', 'phone_number', 'avatar', 'about_me', 'level', 'points')}),
        ('Ruxsatlar', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Muhim sanalar', {'fields': ('last_login', 'date_joined')}),
    )

    # Ro'yxatdan o'tish sahifasida ko'rsatilmaydigan maydonlar
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name')
        }),
    )


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Maxsus User modelini yaratish uchun zarur bo'lgan CustomUserManager klassi
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Elektron pochta manzili kiritilishi shart'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Username maydoni talab qilinmaydi, chunki email asosiy identifikator
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'Admin')  # Superuser har doim Admin bo'ladi

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser is_staff=True bo\'lishi kerak'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser is_superuser=True bo\'lishi kerak'))

        return self.create_user(email, password, **extra_fields)


# Asosiy User modeli
class User(AbstractBaseUser, PermissionsMixin):
    USER_ROLES = [
        ('Admin', 'Admin'),
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
    ]

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True, null=True)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True, null=True)
    about_me = models.TextField(_('about me'), blank=True, null=True)
    points = models.PositiveIntegerField(_('points'), default=0)
    level = models.CharField(_('english level'), max_length=20, default='Beginner')
    role = models.CharField(_('role'), max_length=10, choices=USER_ROLES, default='Student')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
    TokenVerifyView  # Tokenni tekshirish uchun qo'shildi
)
from .views import UserViewSet, PasswordResetView, PasswordResetConfirmView

router = DefaultRouter()
# Foydalanuvchi profilini boshqarish uchun ViewSet ro'yxatga olindi
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Foydalanuvchilar va profilni boshqarish uchun URL'lar
    path('', include(router.urls)),

    # JWT autentifikatsiya uchun maxsus URL manzillar
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Yangi qo'shildi
    path('auth/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # Parolni tiklash URL manzillari
    path('auth/password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('auth/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]

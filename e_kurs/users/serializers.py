from rest_framework import serializers
from .models import User
from django.utils.translation import gettext_lazy as _


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'phone_number',
            'avatar', 'points', 'about_me', 'level', 'role'
        )
        read_only_fields = ('email', 'points', 'role')


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Parolni tiklash so'rovi uchun emailni qabul qiluvchi serializator.
    """
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Parolni tasdiqlash uchun token va yangi parolni qabul qiluvchi serializator.
    """
    new_password = serializers.CharField(min_length=8)
    token = serializers.CharField()
    uid = serializers.CharField()

    def validate(self, attrs):
        # Bu yerda token va uid to'g'riligi tekshirilishi kerak
        # Bu mantiq viewda amalga oshiriladi
        return attrs
